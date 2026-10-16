# Publish the prepared 1.33.0 files

The product version remains 1.33.0. Immutable installation tags distinguish
publication bytes without changing that version or rewriting historical tags.
Use the prepared release directory: it includes the exact plan, script and
assets. The public runtime repository contains the maintained script source;
private build paths and credentials are not needed by the uploader.
The 18 full-bundle assets can be represented by pinned byte slices of the one
local complete ZIP. The uploader creates only the parts currently being sent
and releases their temporary disk space afterward. Separate copies of all
18 parts are unnecessary; the remote Release still provides ordered part files.

Windows PowerShell, from any working directory:

```powershell
& 'PATH-TO-PREPARED-RELEASE/Publish-v1.33.0.ps1'
```

macOS/Linux:

```sh
sh PATH-TO-PREPARED-RELEASE/Publish-v1.33.0.sh
```

Use existing GitHub Git credentials, an existing `gh` login, `GH_TOKEN` or
`GITHUB_TOKEN`. The script never stores credentials in its plan, arguments or
logs. It requires Python 3.10+ and cURL. An explicit proxy is optional:
`-Proxy http://127.0.0.1:PORT` in PowerShell or `--proxy URL` in the shell entry.

The script identifies exact local files, skips remote assets only when the full
SHA-256 and size match, and retries failed uploads within a finite budget. A
failed GitHub Release upload restarts that part; GitHub does not expose a byte
resume operation for an incomplete Release asset. Download clients do resume
owned partial downloads. Rerun the same command after an interruption.

Only matching incomplete starters in the selected draft are replaced. Other
assets, historical tags and unrelated branch changes are preserved. All required
assets must match before releases are made public and `release`/`1.33.0` branches
advance. If publication stops, the previous current entry remains selected;
the plan and uploaded assets support continuation. The two repositories cannot
switch atomically together, so the runtime assets are made public first, and
each branch is advanced without force only from its recorded previous commit.

## 中文

在准备好的发布目录运行 `Publish-v1.33.0.ps1`；macOS/Linux 运行
`sh Publish-v1.33.0.sh`。已有且服务器完整哈希、大小匹配的附件自动跳过。
网络中断后重复同一命令即可继续；只重传未完成的小块。
本地完整 ZIP 可直接作为 18 块的来源，脚本只临时生成正在上传的块，
无需额外保存一整套分块副本；服务器仍然提供逐个可下载的有序分块。

下载支持断点续传；GitHub Release 的未完成上传需要从该块开头重传，
不能把它描述为上传字节级续传。版本仍为 1.33.0，原有历史标签与包保留。
所有附件齐全后才公开 Release 并切换当前分支。发布识别与传输记录不等于
产品测试、运行环境验收或重建效果测量，本修订没有执行这些检查。
