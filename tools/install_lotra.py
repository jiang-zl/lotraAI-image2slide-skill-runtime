#!/usr/bin/env python3
"""One runtime-repository entry. Python 3.12; only stdlib before runtime setup."""
import argparse, hashlib, json, os, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path, PurePosixPath

CHANNEL='https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill-runtime/release/releases/current.json'


def digest(file):
    h=hashlib.sha256()
    with file.open('rb') as source:
        for chunk in iter(lambda:source.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def path(root,name):
    parts=PurePosixPath(name)
    if parts.is_absolute() or not name or '\\' in name or any(p in ('.','..') or ':' in p for p in parts.parts):raise ValueError('Unsafe installer path')
    out=root.joinpath(*parts.parts)
    for p in (out,*out.parents):
        if p==root.parent:break
        if p.is_symlink() or getattr(p,'is_junction',lambda:False)():raise ValueError('Preserve redirected installer path')
    if not out.is_relative_to(root):raise ValueError('Installer escaped project')
    return out


def write(file,data):
    if file.is_file() and file.read_bytes()==data:return
    file.parent.mkdir(parents=True,exist_ok=True)
    temp=file.with_name(file.name+'.entry-part')
    with temp.open('wb') as output:output.write(data)
    os.replace(temp,file)


def request(url,headers=None,limit=2*1024*1024):
    last=None
    for attempt in range(3):
        try:
            transport=urllib.request.build_opener(urllib.request.ProxyHandler({})) if attempt and ('10061' in str(last) or 'refused' in str(last).lower()) else urllib.request.build_opener()
            with transport.open(urllib.request.Request(url,headers={'User-Agent':'lotraAI-install-entry/1.33.0',**(headers or {})}),timeout=60) as response:
                data=response.read(limit+1)
                if len(data)>limit:raise ValueError('Installer metadata exceeds byte limit')
                return data,response.headers.get('ETag')
        except urllib.error.HTTPError as error:
            if error.code==304:return None,None
            last=error
        except OSError as error:last=error
        if attempt<2:time.sleep(2**attempt)
    raise RuntimeError('INSTALL_DOWNLOAD_LIMIT: '+str(last))


def fetch(record,cache):
    file=path(cache,record['sha256'])
    if file.is_file():
        if file.stat().st_size==record['bytes'] and digest(file)==record['sha256']:return file
        raise ValueError('Preserve changed installer cache')
    data,_=request(record['url'],limit=record['bytes'])
    if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:raise ValueError('Installer file hash differs')
    write(file,data);return file


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,required=True)
    args=parser.parse_args();project=args.project.resolve()
    if not project.is_dir() or project in (Path.home().resolve(),Path(project.anchor)):raise ValueError('Choose an existing project directory')
    if sys.version_info[:2]!=(3,12):raise ValueError('Use the runtime repository OS bootstrap for its project-local Python 3.12')
    state=path(project,'.lotraAI-build/install-entry');state.mkdir(parents=True,exist_ok=True)
    channel_file=path(state,'Channel.json');etag_file=path(state,'ETag.txt')
    headers={'If-None-Match':etag_file.read_text()} if channel_file.exists() and etag_file.exists() else {}
    data,etag=request(CHANNEL,headers)
    if data is not None:
        write(channel_file,data)
        if etag:write(etag_file,etag.encode())
    channel=json.loads(channel_file.read_bytes())
    if channel.get('schema')!='lotra-install-channel-1':raise ValueError('Unsupported installation channel')
    cache=path(project,'.lotraAI-build/downloads/sha256');cache.mkdir(parents=True,exist_ok=True)
    entry=channel['entry']
    if digest(Path(__file__).resolve())!=entry['sha256']:
        updated=fetch(entry,cache)
        return subprocess.run([sys.executable,'-I','-X','utf8','-B',str(updated),'--project',str(project)]).returncode
    write(path(state,'Launcher.json'),(json.dumps({'command_prefix':[sys.executable,'-I','-X','utf8','-B',str(Path(__file__).resolve()),'--project',str(project)],
          'entry_sha256':entry['sha256'],'python_sha256':digest(Path(sys.executable).resolve())},sort_keys=True,indent=2)+'\n').encode())
    catalog_file=fetch(channel['catalog'],cache);catalog=json.loads(catalog_file.read_bytes())
    root=path(project,'.lotraAI-build/installers/'+catalog['release_id']);root.mkdir(parents=True,exist_ok=True)
    for name,record in catalog['installer'].items():
        destination=path(root,name)
        if destination.is_file():
            if digest(destination)!=record['sha256']:raise ValueError('Preserve changed installed coordinator')
            continue
        source=None
        for parent in ('releases','installers'):
            history=path(project,'.lotraAI-build/'+parent)
            if history.is_dir():
                for folder in sorted(history.iterdir())[-32:]:
                    prior=path(folder,name)
                    if prior.is_file() and prior.stat().st_size==record['bytes'] and digest(prior)==record['sha256']:
                        source=prior;break
            if source:break
        if source is None:source=fetch(record,cache)
        destination.parent.mkdir(parents=True,exist_ok=True)
        try:os.link(source,destination)
        except OSError:write(destination,source.read_bytes())
    log=path(state,'Install.log')
    with log.open('wb') as stream:
        completed=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(root/'installer/differential.py'),
                                  '--project',str(project),'--catalog',str(catalog_file)],stdout=stream,stderr=subprocess.STDOUT,timeout=2400)
    lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
    result=None
    for line in reversed(lines):
        try:
            value=json.loads(line)
            if isinstance(value,dict) and 'status' in value:result=value;break
        except ValueError:pass
    result=result or {'status':'INSTALL_FAILED'}
    result.setdefault('log',str(log))
    print(json.dumps(result,ensure_ascii=False))
    return completed.returncode


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as error:
        print(json.dumps({'status':'INSTALL_FAILED','reason':str(error)[:300]},ensure_ascii=False));raise SystemExit(1)
