#!/usr/bin/env python3
"""Resume a prepared 1.33.0 publication. Does not run/install/validate the product."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ALLOWED={'jiang-zl/lotraAI-image2slide-skill','jiang-zl/lotraAI-image2slide-skill-runtime'}
PRINT_LOCK=threading.Lock()
PROCESS_LOCK=threading.Lock()
PROCESSES=set()
ABORT=threading.Event()


def log(value):
    with PRINT_LOCK:print(json.dumps(value,ensure_ascii=False),flush=True)


def sha(file):
    h=hashlib.sha256()
    with file.open('rb') as source:
        for block in iter(lambda:source.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()


def local_matches(file,row):
    if file.stat().st_size!=row.get('source_bytes',row['bytes']):return False
    offset=row.get('offset',0);size=row['bytes']
    if offset<0 or size<0 or offset+size>file.stat().st_size:return False
    h=hashlib.sha256()
    with file.open('rb') as source:
        source.seek(offset);left=size
        while left:
            block=source.read(min(left,4*1024*1024))
            if not block:return False
            h.update(block);left-=len(block)
    return h.hexdigest()==row['sha256']


def upload_file(file,row,logs):
    if 'offset' not in row:return file
    handle,name=tempfile.mkstemp(prefix='lotra-part-',suffix='.upload',dir=logs);part=Path(name)
    try:
        with os.fdopen(handle,'wb') as out,file.open('rb') as source:
            source.seek(row['offset']);left=row['bytes']
            while left:
                block=source.read(min(left,4*1024*1024))
                if not block:raise ValueError('Prepared archive ended before its part')
                out.write(block);left-=len(block)
        return part
    except BaseException:
        part.unlink(missing_ok=True);raise


def local(root,name):
    if not name or '\\' in name or any(p in ('','..','.') for p in name.split('/')):raise ValueError('Unsafe publication path')
    file=root/name
    if not file.resolve().is_relative_to(root):raise ValueError('Publication file escaped its prepared directory')
    for parent in (file,*file.parents):
        if parent==root.parent:break
        if parent.is_symlink() or getattr(parent,'is_junction',lambda:False)():raise ValueError('Preserve redirected publication file')
    return file


def credential():
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:return token
    if shutil.which('gh'):
        result=subprocess.run(['gh','auth','token','--hostname','github.com'],capture_output=True,text=True,timeout=30)
        if result.returncode==0 and result.stdout.strip():return result.stdout.strip()
    if shutil.which('git'):
        result=subprocess.run(['git','-c','credential.interactive=never','credential','fill'],
            input='protocol=https\nhost=github.com\n\n',capture_output=True,text=True,timeout=30,
            env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'never','GCM_GUI_PROMPT':'0'})
        if result.returncode==0:
            return next((line.split('=',1)[1] for line in result.stdout.splitlines() if line.startswith('password=')),None)
    raise ValueError('Use existing GitHub credentials, gh auth login, GH_TOKEN or GITHUB_TOKEN; no credential is stored in the plan')


class GitHub:
    def __init__(self,token,proxy):
        self.token=token
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({'https':proxy,'http':proxy} if proxy else {}))

    def api(self,method,path,body=None,missing=False):
        if not any(path=='/repos/'+repo or path.startswith('/repos/'+repo+'/') for repo in ALLOWED):raise ValueError('Unexpected publication repository')
        payload=None if body is None else json.dumps(body).encode()
        request=urllib.request.Request('https://api.github.com'+path,data=payload,method=method,
            headers={'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json',
                     'Content-Type':'application/json','User-Agent':'lotraAI-maintained-publisher/1.33.0'})
        for attempt in range(3):
            if ABORT.is_set():raise InterruptedError('Publication stopped; uploaded assets retained')
            try:
                with self.opener.open(request,timeout=45) as response:
                    data=response.read(16*1024*1024)
                    return json.loads(data) if data else None
            except urllib.error.HTTPError as error:
                if missing and error.code==404:return None
                if error.code not in (429,500,502,503,504) or attempt==2:raise RuntimeError('GitHub HTTP '+str(error.code)+' '+method+' '+path) from None
            except OSError:
                if attempt==2:raise RuntimeError('GitHub connection failed: '+method+' '+path) from None
            time.sleep(2**attempt)

    def assets(self,repo,release_id):
        rows=[];page=1
        while True:
            found=self.api('GET','/repos/'+repo+'/releases/'+str(release_id)+'/assets?per_page=100&page='+str(page))
            rows.extend(found)
            if len(found)<100:return rows
            page+=1


def release(client,group,root):
    base='/repos/'+group['repository'];tag=group['tag']
    found=client.api('GET',base+'/releases/tags/'+tag,missing=True)
    if found:return found
    for found in client.api('GET',base+'/releases?per_page=100'):
        if found['tag_name']==tag:return found
    body=local(root,group['notes']).read_text(encoding='utf-8')
    return client.api('POST',base+'/releases',{'tag_name':tag,'name':group['name'],
        'body':body,'draft':True,'prerelease':group.get('prerelease',False)})


def matching(asset,row):
    return asset.get('state')=='uploaded' and asset.get('size')==row['bytes'] and asset.get('digest')=='sha256:'+row['sha256']


def upload(client,group,rel,row,root,curl,logs,proxy,retries,timeout):
    repo=group['repository'];file=local(root,row['path']);name=row['name']
    for attempt in range(1,retries+1):
        if ABORT.is_set():raise InterruptedError('Publication stopped')
        existing=next((asset for asset in client.assets(repo,rel['id']) if asset['name']==name),None)
        if existing:
            if matching(existing,row):return {'repository':repo,'tag':group['tag'],'name':name,'state':'retained','sha256':row['sha256']}
            if rel['draft'] and existing['state']=='starter' and existing.get('digest') is None and existing['size'] in (0,row['bytes']):
                client.api('DELETE','/repos/'+repo+'/releases/assets/'+str(existing['id']))
            else:raise ValueError('Preserve conflicting remote asset: '+name)
        if not local_matches(file,row):raise ValueError('Prepared upload file changed: '+name)
        url=rel['upload_url'].split('{',1)[0]
        parsed=urllib.parse.urlsplit(url)
        if parsed.scheme!='https' or parsed.hostname!='uploads.github.com':raise ValueError('Unexpected upload host')
        stamp=name+'.'+str(time.time_ns());response=logs/(stamp+'.response.json');error_log=logs/(stamp+'.log')
        if any(c in client.token for c in '\r\n"\\'):raise ValueError('Unexpected credential format')
        transfer=upload_file(file,row,logs)
        command=[curl,'--config','-','--request','POST','--upload-file',str(transfer),
            '--header','Content-Type: application/octet-stream','--header','Accept: application/vnd.github+json',
            '--header','Expect: 100-continue','--expect100-timeout','5','--connect-timeout','30',
            '--max-time',str(timeout),'--speed-limit','1024','--speed-time','90','--silent','--show-error',
            '--output',str(response),'--stderr',str(error_log),'--write-out','%{http_code}',
            *(['--proxy',proxy] if proxy else ['--noproxy','*']),url+'?name='+urllib.parse.quote(name,safe='')]
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        with PROCESS_LOCK:PROCESSES.add(process)
        try:
            status,_=process.communicate(('header = "Authorization: Bearer '+client.token+'"\n').encode(),timeout=timeout+30)
            if process.returncode or status.strip()!=b'201':raise RuntimeError('Upload interrupted/failed; log '+str(error_log))
            saved=json.loads(response.read_bytes())
            if not matching(saved,row):raise ValueError('Uploaded asset identity differs: '+name)
            return {'repository':repo,'tag':group['tag'],'name':name,'state':'uploaded','sha256':row['sha256']}
        except (RuntimeError,OSError,subprocess.TimeoutExpired) as error:
            if attempt==retries:raise RuntimeError('Upload limit reached for '+name+'; rerun the same publication command') from error
            log({'phase':'ASSET_RETRY','name':name,'attempt':attempt+1})
            time.sleep(min(2**attempt,4))
        finally:
            if process.poll() is None:process.kill();process.communicate()
            with PROCESS_LOCK:PROCESSES.discard(process)
            if transfer!=file:transfer.unlink(missing_ok=True)


def refs(client,plan,*,advance=False):
    facts=[]
    for item in plan['repositories']:
        repo=item['repository'];base='/repos/'+repo
        ref=client.api('GET',base+'/git/ref/tags/'+plan['tag'])['object']
        if ref['type']=='tag':ref=client.api('GET',base+'/git/tags/'+ref['sha'])['object']
        if ref['type']!='commit' or ref['sha']!=item['commit']:raise ValueError('Preserve a tag bound to another commit')
        for branch,previous in item['previous_branches'].items():
            current=client.api('GET',base+'/git/ref/heads/'+branch)['object']['sha']
            if current not in (previous,item['commit']):raise ValueError('Preserve changed current branch: '+repo+'/'+branch)
            if advance and current!=item['commit']:
                client.api('PATCH',base+'/git/refs/heads/'+branch,{'sha':item['commit'],'force':False})
                if client.api('GET',base+'/git/ref/heads/'+branch)['object']['sha']!=item['commit']:raise ValueError('Current branch publication incomplete')
        facts.append({'repository':repo,'commit':item['commit']})
    return facts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('Publish-plan.json'))
    parser.add_argument('--publish',action='store_true',help='Publish releases and advance current branches after all assets match')
    parser.add_argument('--jobs',type=int,choices=range(1,5),default=2)
    parser.add_argument('--retries',type=int,choices=range(1,4),default=2)
    parser.add_argument('--upload-timeout',type=int,default=900)
    parser.add_argument('--proxy',default='',help='Optional explicit HTTPS proxy')
    args=parser.parse_args();root=args.plan.resolve().parent;plan=json.loads(args.plan.read_bytes())
    if plan.get('schema')!='lotra-prepared-publication-1' or plan.get('version')!='1.33.0':raise ValueError('Unsupported prepared publication')
    if not 60<=args.upload_timeout<=3600:raise ValueError('Upload timeout must be 60..3600 seconds')
    curl=shutil.which('curl.exe') or shutil.which('curl')
    if not curl:raise ValueError('cURL is required for bounded asset uploads')
    groups=plan['groups']
    if any(group['repository'] not in ALLOWED or not re.fullmatch(r'v1\.33\.0-install-r[34]',group['tag']) for group in groups):raise ValueError('Unexpected publication target')
    if {row['repository'] for row in plan['repositories']}!=ALLOWED:raise ValueError('Unexpected branch publication scope')
    for group in groups:
        names=set()
        for row in group['assets']:
            if not re.fullmatch(r'[A-Za-z0-9_.-]+',row['name']) or row['name'] in names:raise ValueError('Unsafe/duplicate asset name')
            names.add(row['name']);file=local(root,row['path'])
            if not local_matches(file,row):raise ValueError('Prepared file identity differs: '+row['name'])
    token=credential()
    if not token:raise ValueError('GitHub publication credential unavailable')
    client=GitHub(token,args.proxy);refs(client,plan)
    releases={i:release(client,g,root) for i,g in enumerate(groups)}
    logs=local(root,'Upload-logs');logs.mkdir(exist_ok=True);progress=local(root,'Upload-progress-v133.json')
    completed=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as workers:
        futures=[workers.submit(upload,client,g,releases[i],row,root,curl,logs,args.proxy,args.retries,args.upload_timeout)
                 for i,g in enumerate(groups) for row in sorted(g['assets'],key=lambda row:(row['bytes'],row['name']))]
        try:
            for future in as_completed(futures):
                record=future.result();completed.append(record)
                temporary=progress.with_suffix('.json.part');temporary.write_text(json.dumps(completed,indent=2)+'\n',encoding='utf-8');os.replace(temporary,progress)
                log({'phase':'ASSET_COMPLETE','completed':len(completed),'total':len(futures),'name':record['name'],'state':record['state']})
        except BaseException:
            ABORT.set()
            with PROCESS_LOCK:
                for process in list(PROCESSES):
                    if process.poll() is None:process.kill()
            for future in futures:future.cancel()
            raise
    for i,group in enumerate(groups):
        actual={asset['name']:asset for asset in client.assets(group['repository'],releases[i]['id'])}
        if any(row['name'] not in actual or not matching(actual[row['name']],row) for row in group['assets']):raise ValueError('Publication assets incomplete')
    refs(client,plan)
    if args.publish:
        for i,group in enumerate(groups):
            rel=releases[i]
            body=local(root,group['notes']).read_text(encoding='utf-8')
            client.api('PATCH','/repos/'+group['repository']+'/releases/'+str(rel['id']),
                {'draft':False,'prerelease':group.get('prerelease',False),'name':group['name'],'body':body,'make_latest':'false' if group.get('prerelease') else 'true'})
        facts=refs(client,plan,advance=True)
    else:facts=refs(client,plan)
    result={'status':'PUBLISHED' if args.publish else 'ASSETS_UPLOADED_CURRENT_BRANCHES_UNCHANGED','version':'1.33.0',
            'tag':plan['tag'],'publication_revision':plan['publication_revision'],'repositories':facts,
            'releases':[{'repository':g['repository'],'url':releases[i]['html_url']} for i,g in enumerate(groups)],
            'asset_count':len(completed),'product_execution':False,'product_checks':'NOT_RUN_PER_USER_REQUEST'}
    local(root,'Publication.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    log(result)


if __name__=='__main__':
    try:main()
    except (Exception,KeyboardInterrupt) as error:
        log({'status':'PUBLICATION_PENDING','version':'1.33.0','reason':str(error)[:350],
             'next_action':'Rerun the same prepared publication command; matching uploaded assets are retained','product_execution':False})
        raise SystemExit(1)
