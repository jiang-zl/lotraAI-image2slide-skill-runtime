#!/usr/bin/env python3
"""Compatibility entry for complete bundles; the official installer owns transport."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

CHANNEL='https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill-runtime/release/releases/current.json'


def read(url,limit):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'lotraAI-bundle-entry/1.34.0'}),timeout=60) as response:
        data=response.read(limit+1)
    if len(data)>limit:raise ValueError('Installation entry exceeds its byte limit')
    return data


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=Path.cwd())
    parser.add_argument('--output-dir',type=Path,default=Path('downloads'))
    args=parser.parse_args()
    if sys.version_info[:2]!=(3,12):raise ValueError('Use the repository OS bootstrap, or its prepared Python 3.12')
    project=args.project.resolve()
    if not project.is_dir() or project in (Path.home().resolve(),Path(project.anchor)):raise ValueError('Choose an existing project directory')
    channel=json.loads(read(CHANNEL,2*1024*1024))
    if channel.get('schema')!='lotra-install-channel-1':raise ValueError('Unsupported installation channel')
    record=channel['entry'];digest=record['sha256']
    if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('Invalid entry identity')
    if not 0<record['bytes']<256*1024:raise ValueError('Unexpected entry size')
    root=project/'.lotraAI-build/bootstrap'/digest
    cursor=root
    while cursor!=project.parent:
        if cursor.is_symlink() or getattr(cursor,'is_junction',lambda:False)():raise ValueError('Preserve redirected installer storage')
        cursor=cursor.parent
    root.mkdir(parents=True,exist_ok=True);entry=root/'install_lotra.py'
    if entry.exists():
        if hashlib.sha256(entry.read_bytes()).hexdigest()!=digest:raise ValueError('Preserve changed installation entry')
    else:
        data=read(record['url'],record['bytes'])
        if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=digest:raise ValueError('Installation entry identity differs')
        with entry.open('xb') as stream:stream.write(data)
    return subprocess.run([sys.executable,'-I','-X','utf8','-B',str(entry),'--project',str(project),
                           '--download-bundle',str(args.output_dir.resolve())]).returncode


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as error:
        print(json.dumps({'status':'BUNDLE_DOWNLOAD_FAILED','reason':str(error)[:300]}));raise SystemExit(1)
