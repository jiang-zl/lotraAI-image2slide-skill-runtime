#!/usr/bin/env python3
"""Download/reassemble the single complete lotraAI bundle from release parts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import urllib.parse
import urllib.request

DEFAULT_MANIFEST = "https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/download/v1.31.0/v1.31.0.json"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_name(name):
    if not isinstance(name, str) or not name or Path(name).name != name or name in (".", "..") or "\\" in name or ":" in name:
        raise ValueError("Unsafe bundle/part filename")
    return name

def open_https(url):
    u = urllib.parse.urlsplit(url)
    if u.scheme != "https" or u.hostname not in ("github.com", "raw.githubusercontent.com"):
        raise ValueError("Expected an HTTPS GitHub release URL")
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"lotraAI-bundle-downloader"}), timeout=120)

def get_manifest(value):
    if value.startswith("https://"):
        with open_https(value) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError("Manifest is too large")
        return json.loads(raw)
    return json.loads(Path(value).read_text(encoding="utf-8"))

def assemble(manifest, output_dir, parts_dir=None):
    if manifest.get("schema") != "lotraai-publication-release-1" or manifest.get("version") != "1.31.0":
        raise ValueError("Unsupported product manifest")
    bundle = manifest["bundle"]
    name = safe_name(bundle["filename"])
    parts = bundle["parts"]
    if [p["index"] for p in parts] != list(range(1, len(parts) + 1)):
        raise ValueError("Parts must have a complete, ordered index")
    if len({safe_name(p["filename"]) for p in parts}) != len(parts):
        raise ValueError("Duplicate part filenames")
    if sum(p["bytes"] for p in parts) != bundle["bytes"]:
        raise ValueError("Part sizes do not match the complete bundle")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / name
    if output.is_symlink():
        raise ValueError("Preserve a redirected output")
    if output.exists():
        if output.stat().st_size == bundle["bytes"] and sha(output) == bundle["sha256"]:
            print("Already verified: " + str(output))
            return output
        raise ValueError("Preserve an existing different output: " + str(output))
    scratch = output_dir / (name + ".assembling")
    if scratch.exists() or scratch.is_symlink():
        raise ValueError("Preserve an existing assembly checkpoint: " + str(scratch))
    total_hash = hashlib.sha256()
    try:
        with scratch.open("xb") as dest:
            for part in parts:
                part_name = safe_name(part["filename"])
                if parts_dir:
                    path = parts_dir / part_name
                    if path.is_symlink():
                        raise ValueError("Preserve a redirected part")
                    source = path.open("rb")
                else:
                    source = open_https(part["url"])
                h, count = hashlib.sha256(), 0
                print("Reading part " + str(part["index"]) + "/" + str(len(parts)), flush=True)
                with source:
                    for block in iter(lambda: source.read(4 * 1024 * 1024), b""):
                        count += len(block)
                        if count > part["bytes"]:
                            raise ValueError("Part exceeds declared size")
                        h.update(block)
                        total_hash.update(block)
                        dest.write(block)
                if count != part["bytes"] or h.hexdigest() != part["sha256"]:
                    raise ValueError("Part integrity check failed: " + part_name)
        if scratch.stat().st_size != bundle["bytes"] or total_hash.hexdigest() != bundle["sha256"]:
            raise ValueError("Complete bundle integrity check failed")
        # A hard link publishes only this verified new file and refuses a concurrent target.
        os.link(scratch, output)
        scratch.unlink()
    except BaseException:
        if scratch.is_file() and not scratch.is_symlink():
            scratch.unlink()
        raise
    print("Complete bundle verified: " + str(output), flush=True)
    return output

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default=DEFAULT_MANIFEST)
    p.add_argument("--output-dir", type=Path, default=Path.cwd())
    p.add_argument("--parts-dir", type=Path, help="Use already downloaded local parts")
    args = p.parse_args()
    assemble(get_manifest(args.manifest), args.output_dir, args.parts_dir)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Bundle preparation stopped: " + str(e), file=sys.stderr)
        raise SystemExit(1)
