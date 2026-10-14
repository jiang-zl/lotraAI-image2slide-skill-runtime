#!/usr/bin/env python3
"""Upload the prepared complete-bundle parts, verify them, and optionally publish."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
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

ROOT = Path(__file__).resolve().parent.parent
PRINT_LOCK = threading.Lock()
PROCESS_LOCK = threading.Lock()
PROCESSES = set()
ABORT = threading.Event()

def log(message):
    with PRINT_LOCK:
        print(message, flush=True)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(4*1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def local(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('A publication path leaves the runtime project')
    return path

def matches(asset, row):
    return (asset.get('state') == 'uploaded' and asset.get('size') == row['bytes']
            and asset.get('digest') == 'sha256:'+row['sha256'])

def load_assets(root, plan):
    manifest_path = local(root, plan['manifest'])
    if sha(manifest_path) != plan['manifest_sha256']:
        raise ValueError('The prepared version manifest changed')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    bundle = manifest['bundle']
    parts = bundle['parts']
    if not parts or [p['index'] for p in parts] != list(range(1,len(parts)+1)):
        raise ValueError('Parts are not a complete ordered sequence')
    rows, full, count, names = [], hashlib.sha256(), 0, set()
    for p in parts:
        name = p['filename']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+',name) or name in names:
            raise ValueError('Unsafe or duplicate asset name')
        names.add(name)
        path = local(root, plan['parts_dir']+'/'+name)
        h, size = hashlib.sha256(), 0
        with path.open('rb') as source:
            for block in iter(lambda: source.read(4*1024*1024), b''):
                h.update(block)
                full.update(block)
                size += len(block)
        if size != p['bytes'] or h.hexdigest() != p['sha256'] or size > 128*1024*1024:
            raise ValueError('Part identity/size mismatch: '+name)
        count += size
        rows.append({**p,'path':path})
    if count != bundle['bytes'] or full.hexdigest() != bundle['sha256']:
        raise ValueError('Reassembled complete-bundle identity mismatch')
    helper = local(root, plan['download_helper'])
    if sha(helper) != plan['download_helper_sha256']:
        raise ValueError('The prepared download helper changed')
    for path in (manifest_path, helper):
        rows.append({'filename':path.name,'path':path,'bytes':path.stat().st_size,'sha256':sha(path)})
    log(f'LOCAL OK: {len(parts)} parts; complete ZIP {count:,} bytes; SHA-256 {full.hexdigest()}')
    return rows

def credential():
    for name in ('GH_TOKEN','GITHUB_TOKEN'):
        if os.environ.get(name):
            return os.environ[name]
    if shutil.which('gh'):
        p = subprocess.run(['gh','auth','token','--hostname','github.com'], capture_output=True, text=True, timeout=30)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    env = {**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'Never'}
    for command in ('git','git.exe'):
        binary = shutil.which(command)
        if not binary:
            continue
        try:
            p = subprocess.run([binary,'-c','credential.interactive=never','credential','fill'],
                input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True, env=env, timeout=30)
        except subprocess.TimeoutExpired:
            continue
        fields = dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
        if p.returncode == 0 and fields.get('password'):
            return fields['password']
    raise RuntimeError('No GitHub API credential found. Run this on Windows with existing Git credentials, or use gh auth login. SSH git authentication alone cannot upload Release assets.')

class GitHub:
    def __init__(self, secret, owner, repositories, proxy=None):
        self.secret, self.owner, self.repositories = secret, owner, set(repositories)
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https':proxy,'http':proxy} if proxy else {}))
        self.lock = threading.Lock()

    def request(self, path, method='GET', data=None, missing=False):
        if path != '/user' and not any(path == f'/repos/{self.owner}/{r}' or path.startswith(f'/repos/{self.owner}/{r}/') for r in self.repositories):
            raise ValueError('Request outside the configured repositories')
        payload = None if data is None else json.dumps(data).encode()
        request = urllib.request.Request('https://api.github.com'+path, data=payload, method=method,
            headers={'Authorization':'Bearer '+self.secret,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'lotraAI-release-publisher'})
        with self.lock:
            for attempt in range(4):
                if ABORT.is_set():
                    raise InterruptedError('Publication interrupted')
                try:
                    with self.opener.open(request,timeout=30) as response:
                        raw = response.read(16*1024*1024)
                        return json.loads(raw) if raw else None
                except urllib.error.HTTPError as e:
                    if missing and e.code == 404:
                        return None
                    if e.code not in (429,500,502,503,504) or attempt == 3:
                        raise RuntimeError(f'GitHub API HTTP {e.code}: {method} {path}') from None
                except (OSError,urllib.error.URLError):
                    if attempt == 3:
                        raise RuntimeError('GitHub API connection failed: '+method+' '+path) from None
                log(f'API retry {attempt+1}/3: {method} {path}')
                time.sleep(2*(attempt+1))

    def assets(self, base, release_id):
        rows, page = [], 1
        while True:
            batch = self.request(f'{base}/releases/{release_id}/assets?per_page=100&page={page}')
            rows.extend(batch)
            if len(batch) < 100:
                return rows
            page += 1

def preflight(client, plan):
    if client.request('/user')['login'] != plan['owner']:
        raise ValueError('The GitHub credential belongs to a different account')
    releases = {}
    for item in plan['repositories']:
        base = '/repos/'+plan['owner']+'/'+item['name']
        repo = client.request(base)
        if not repo.get('permissions',{}).get('push') or repo['default_branch'] != 'release':
            raise ValueError('Repository permissions/default branch differ: '+item['name'])
        for branch in ('1.31.0','release'):
            if client.request(base+'/branches/'+branch)['commit']['sha'] != item['commit']:
                raise ValueError('Published source branch changed: '+item['name']+'/'+branch)
        ref = client.request(base+'/git/ref/tags/'+plan['tag'])['object']
        if ref['type'] == 'tag':
            ref = client.request(base+'/git/tags/'+ref['sha'])['object']
        if ref['type'] != 'commit' or ref['sha'] != item['commit']:
            raise ValueError('Published source tag changed: '+item['name'])
        release = client.request(base+'/releases/'+str(item['release_id']))
        if release['tag_name'] != plan['tag']:
            raise ValueError('Unexpected release tag')
        releases[item['name']] = release
        log('REMOTE OK: '+item['name']+' '+item['commit'][:12]+(' (draft)' if release['draft'] else ' (published)'))
    return releases

def retire_prepared_assets(client, plan, base, release):
    current = {x['id']:x for x in client.assets(base,release['id'])}
    selected = []
    for old in plan['retire_assets']:
        actual = current.get(old['id'])
        if actual:
            if any(actual.get(k) != old.get(k) for k in ('name','state','size','digest')):
                raise ValueError('Preserve changed legacy asset: '+old['name'])
            selected.append(actual)
    if selected and not release['draft']:
        raise ValueError('Preserve assets of an already published release')
    for old in selected:
        client.request(base+'/releases/assets/'+str(old['id']),'DELETE',missing=True)
        log('Retired this task\'s superseded asset: '+old['name'])

def curl_upload(curl, row, release, secret, log_dir, proxy, attempt):
    name = row['filename']
    url = release['upload_url'].split('{')[0]
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'uploads.github.com':
        raise ValueError('Unexpected upload host')
    url += '?name='+urllib.parse.quote(name,safe='')
    stamp = str(time.time_ns())
    response_path = log_dir/(name+'.'+stamp+'.response.json')
    progress_path = log_dir/(name+'.'+stamp+'.progress.log')
    if any(c in secret for c in ('\r','\n','"','\\')):
        raise ValueError('Unsupported credential format')
    command = [curl,'--config','-','--request','POST','--upload-file',str(row['path']),
        '--header','Content-Type: application/octet-stream','--header','Accept: application/vnd.github+json',
        '--header','Expect: 100-continue','--expect100-timeout','5','--connect-timeout','30',
        '--speed-limit','1024','--speed-time','90','--progress-bar','--output',str(response_path),
        '--stderr',str(progress_path),'--write-out','%{http_code}\n']
    features = subprocess.run([curl,'--version'],capture_output=True,text=True,check=True).stdout
    if 'HTTP2' in features:
        command.append('--http2')
    command.extend(['--proxy',proxy] if proxy else ['--noproxy','*'])
    command.append(url)
    proc = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    with PROCESS_LOCK:
        PROCESSES.add(proc)
    try:
        proc.stdin.write(('header = "Authorization: Bearer '+secret+'"\n').encode())
        proc.stdin.close()
        log(f'UPLOAD {name} (attempt {attempt})')
        previous, last = None, time.monotonic()
        while proc.poll() is None:
            time.sleep(1)
            if time.monotonic()-last < 15:
                continue
            last = time.monotonic()
            if progress_path.exists():
                with progress_path.open('rb') as stream:
                    stream.seek(max(0,progress_path.stat().st_size-65536))
                    found = re.findall(r'(\d+(?:\.\d+)?)%',stream.read().decode(errors='replace'))
                percent = found[-1] if found else None
                if percent != previous:
                    log(name+': '+str(percent)+'%')
                    previous = percent
        status = proc.stdout.read().decode(errors='replace').strip()
        if proc.returncode != 0 or status != '201':
            raise RuntimeError(f'cURL exit {proc.returncode}, HTTP {status or "unavailable"}; log {progress_path}')
        saved = json.loads(response_path.read_text(encoding='utf-8'))
        if not matches(saved,row):
            raise ValueError('Server asset digest mismatch: '+name)
        return saved
    finally:
        with PROCESS_LOCK:
            PROCESSES.discard(proc)
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=10)

def upload_one(client, base, release, row, curl, log_dir, proxy, retries):
    name = row['filename']
    for attempt in range(1,retries+1):
        if ABORT.is_set():
            raise InterruptedError('Publication interrupted')
        old = next((x for x in client.assets(base,release['id']) if x['name'] == name),None)
        if old and matches(old,row):
            log('SKIP verified: '+name)
            return old
        if not release['draft']:
            raise ValueError('Preserve an already published release with a different/missing asset')
        if old:
            if old['state'] != 'starter' or old['size'] != row['bytes'] or old.get('digest') is not None:
                raise ValueError('Preserve unexpected existing asset: '+name)
            client.request(base+'/releases/assets/'+str(old['id']),'DELETE',missing=True)
        try:
            saved = curl_upload(curl,row,release,client.secret,log_dir,proxy,attempt)
            log('VERIFIED '+name+' '+saved['digest'])
            return saved
        except (RuntimeError,OSError) as error:
            if ABORT.is_set():
                raise InterruptedError('Publication interrupted')
            # A dropped response may follow a successful server-side upload.
            actual = next((x for x in client.assets(base,release['id']) if x['name'] == name),None)
            if actual and matches(actual,row):
                log('VERIFIED after response loss: '+name)
                return actual
            if attempt == retries:
                raise
            log(str(error)+'; retrying only this part')
            time.sleep(3*attempt)

def verify_remote_assets(client, base, release, rows):
    actual = {x['name']:x for x in client.assets(base,release['id'])}
    for row in rows:
        if row['filename'] not in actual or not matches(actual[row['filename']],row):
            raise ValueError('Remote complete asset check failed: '+row['filename'])
    return [actual[row['filename']] for row in rows]

@contextmanager
def publication_lock(path):
    if os.name == 'nt':
        # WSL's UNC provider does not support Windows byte-range file locks.
        directory = Path(tempfile.gettempdir())/'lotraAI-release-publisher-locks'
        directory.mkdir(exist_ok=True)
        key = hashlib.sha256(str(path.resolve()).casefold().encode()).hexdigest()
        path = directory/(key+'.lock')
    with path.open('a+b') as handle:
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            if path.stat().st_size == 0:
                handle.write(b'0')
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        yield

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=3,help='Parallel uploads (1-6; default 3)')
    parser.add_argument('--retries',type=int,default=3,help='Attempts per failed part (default 3)')
    parser.add_argument('--check-local',action='store_true',help='Verify local parts only; no network')
    parser.add_argument('--check',action='store_true',help='Verify local files, authentication, branches and drafts; no writes')
    parser.add_argument('--publish',action='store_true',help='Publish both releases only after all assets verify')
    parser.add_argument('--proxy',help='Optional explicit HTTP proxy URL; default direct/TUN connection')
    args = parser.parse_args()
    if not 1 <= args.jobs <= 6 or not 1 <= args.retries <= 10:
        parser.error('Use 1-6 jobs and 1-10 attempts')
    work = ROOT/'.lotraAI-build/publication'
    plan = json.loads((work/'upload-plan-v1.31.0.json').read_text(encoding='utf-8'))
    with publication_lock(work/'publish-v1.31.0.lock'):
        rows = load_assets(ROOT,plan)
        if args.check_local:
            return
        client = GitHub(credential(),plan['owner'],[r['name'] for r in plan['repositories']],args.proxy)
        releases = preflight(client,plan)
        if args.check:
            log('CHECK OK: no remote changes made')
            return
        curl = shutil.which('curl.exe' if os.name == 'nt' else 'curl')
        if not curl:
            raise RuntimeError('cURL is required')
        runtime = plan['runtime_repository']
        release = releases[runtime]
        base = '/repos/'+plan['owner']+'/'+runtime
        retire_prepared_assets(client,plan,base,release)
        log_dir = work/'upload-logs'
        log_dir.mkdir(exist_ok=True)
        completed, failures = [], []
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(upload_one,client,base,release,row,curl,log_dir,args.proxy,args.retries):row for row in rows}
            try:
                for future in as_completed(futures):
                    try:
                        completed.append(future.result())
                    except Exception as error:
                        failures.append(futures[future]['filename']+': '+str(error))
                        log('FAILED '+failures[-1])
            except BaseException:
                ABORT.set()
                for future in futures:
                    future.cancel()
                with PROCESS_LOCK:
                    for proc in list(PROCESSES):
                        proc.terminate()
                raise
        if failures:
            raise RuntimeError('Some parts failed. Rerun the same command; verified parts will be skipped.\n'+'\n'.join(failures))
        saved = verify_remote_assets(client,base,release,rows)
        receipt = {'verified_at':datetime.now(timezone.utc).isoformat(),'tag':plan['tag'],
                   'assets':[{'name':x['name'],'id':x['id'],'bytes':x['size'],'digest':x['digest']} for x in saved],
                   'status':'ASSETS_VERIFIED','functional_validation':'NOT_RUN_PER_USER_REQUEST'}
        (work/'Upload-result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        log('ALL ASSETS VERIFIED')
        if not args.publish:
            log('Releases remain drafts. Rerun with --publish to publish both.')
            return
        # Recheck source refs after the potentially long upload; publish runtime first.
        releases = preflight(client,plan)
        urls = []
        for item in sorted(plan['repositories'],key=lambda r:r['name'] != runtime):
            current = releases[item['name']]
            if current['draft']:
                current = client.request('/repos/'+plan['owner']+'/'+item['name']+'/releases/'+str(item['release_id']),'PATCH',
                    {'body':local(ROOT,item['notes']).read_text(encoding='utf-8'),'target_commitish':item['commit'],
                     'draft':False,'prerelease':False,'make_latest':'true'})
            if current['draft'] or current['tag_name'] != plan['tag']:
                raise ValueError('Release publication did not complete')
            urls.append(current['html_url'])
            log('PUBLISHED '+current['html_url'])
        receipt.update(status='RELEASES_PUBLISHED',release_urls=urls)
        (work/'Upload-result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        with PROCESS_LOCK:
            for proc in list(PROCESSES):
                proc.terminate()
        log('Interrupted. Rerun the same command to retain verified uploaded parts.')
        raise SystemExit(130)
    except Exception as error:
        log('STOPPED: '+str(error))
        raise SystemExit(1)
