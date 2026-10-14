# Publish the prepared v1.31.0 release

The complete ZIP is transported as 18 ordered parts, each no larger than 128 MiB. The last part is slightly smaller. The assembled file remains `lotraAI-image2slide-v1.31.0-bundle.zip`, including the skill and runtime resources.

The local preparation includes `.lotraAI-build/publication/upload-plan-v1.31.0.json` and the actual part files. These private files are intentionally excluded from Git. A fresh clone alone does not contain the binary upload inputs.

## Run on Windows with your VPN

Open PowerShell and run:

```powershell
Set-Location '\\wsl.localhost\Ubuntu\home\jiangzl\lotraAI-runtime'
py -3 .\tools\publish_release.py --jobs 3 --publish
```

The equivalent WSL command is:

```bash
cd /home/jiangzl/lotraAI-runtime
bash scripts/publish-v1.31.0.sh --jobs 3 --publish
```

Python 3 and cURL are required. The uploader uses the current machine's direct/TUN route by default. For an explicit HTTP proxy, append `--proxy http://127.0.0.1:YOUR_PORT`, replacing `YOUR_PORT` with your VPN client's actual HTTP proxy port. It does not change system network settings.

## Authentication

SSH authentication is used for Git branch/tag pushes. Release assets use GitHub's HTTPS API and need an API login. The script tries `GH_TOKEN`/`GITHUB_TOKEN`, an existing `gh` login, and Git's saved HTTPS credentials, including `git.exe` from WSL when available. On this prepared Windows host, the saved Git credential was verified during publication preparation.

If no usable API credential is available, use `gh auth login --hostname github.com` on the machine running the script, or run the Windows command where your Git credentials are already available. Credentials are kept in memory and passed to cURL through standard input. They are not placed in the script, process arguments, or upload logs.

## Checks and recovery

```bash
# Local part hashes and the complete reassembled ZIP hash; no network.
python3 tools/publish_release.py --check-local

# Also check API authentication, both branches, tags, and releases; no remote writes.
python3 tools/publish_release.py --check

# Upload and verify assets, keeping both releases as drafts.
python3 tools/publish_release.py --jobs 3

# Upload, verify all assets, then publish runtime followed by skill.
python3 tools/publish_release.py --jobs 3 --publish
```

Run one upload instance at a time. Rerun the same command after a network interruption: completed parts are skipped only when GitHub's full SHA-256 and byte count match. A failed part restarts from its beginning, with three attempts by default. `--jobs` accepts 1–6 and `--retries` accepts 1–10.

The preparation records the exact IDs, sizes, states, and digests of this task's superseded draft assets. Upload mode removes only those unchanged old assets before replacing the transport plan. Unexpected existing complete assets are preserved and stop the operation. Check modes do not remove assets.

The uploader rechecks source branches/tags before publishing and publishes only after all 18 parts, the version manifest, and `fetch_bundle.py` have matching server digests. Logs and `Upload-result.json` are saved under `.lotraAI-build/publication`. Existing source history and the `sci-rebuild` development checkout are outside this upload.

## 中文说明

完整包已分为 **18 块，每块最多 128 MiB**。推荐在已开启 VPN 的 Windows PowerShell 中运行上面的 `py -3 ... --jobs 3 --publish` 命令；也可在 WSL 中运行 Bash 入口。

脚本会先校验本地分块及整包 SHA-256，再核对两个仓库的版本分支、release 分支和标签。成功上传的分块会按 GitHub 返回的完整 SHA-256 与大小校验，重复执行会跳过已完成分块。失败时只重传对应小块。

`--publish` 表示全部附件校验成功后，依次公开 runtime 与 skill 的两个 Release。省略它则仅上传并保留草稿。`--check` 用于只读预检，`--check-local` 不访问网络。

Git SSH 免密用于推送源码；Release 附件通过 HTTPS API 上传。脚本优先复用已有登录，Windows 中会读取 Git 已保存的 GitHub 凭据，不需要把 token 写进脚本。旧传输方案附件仅按本次任务记录的精确身份替换。完整 ZIP、运行资源和开发目录保持原样。

The product's functional validation remains `NOT_RUN_PER_USER_REQUEST`. These are publication and transport checks.
