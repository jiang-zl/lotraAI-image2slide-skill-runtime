# 安装与更新

[English](installation.md) · [返回首页](../README.zh-CN.md)

## 推荐方式

在 Codex 的工作项目中发送：

> 请从 https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime 在当前项目安装或更新 lotraAI Image2Slide。

已有安装优先复用 `.lotraAI-build/install-entry/Launcher.json`。首次安装由系统入口准备所需的私有 Python，再调用共同安装程序。安装资源准备完成后登记一个主 skill，入口为 `.agents/skills/lotra-image2slide-skill/SKILL.md`。

安装器不要求先全局安装 Python 或运行全局 pip，也不需要额外模型 API key。Codex 与用于查看、编辑 PPTX 的软件由用户自行提供。

## 手动运行入口

以下命令在已取得本仓库文件的目录执行。将示例路径替换为**已经存在的工作项目目录**，不要把用户主目录或磁盘根目录当成项目。

Windows PowerShell：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_lotra.ps1 -Project 'C:\work\my-project'
```

macOS / Linux / WSL：

```sh
sh tools/install_lotra.sh '/absolute/path/to/my-project'
```

更新仍使用同一入口。程序新增新文件、替换变化文件、移除新版删除的受管理文件；内容不变的生效文件不重新下载或写入。被自行改动或归属不明的文件会保留并报告冲突。个人知识库、字体、任务、原图、PPT 和全局技能保留。

## 完整包与本地安装

完整包由清单规定的 18 个有序分块组成，下载程序负责续传、逐块校验、合并与整包校验。需要先下载到指定位置时，可使用：

Windows：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_lotra.ps1 -Project 'C:\work\my-project' -DownloadBundle 'C:\downloads\lotraAI'
```

macOS / Linux / WSL：

```sh
sh tools/install_lotra.sh '/absolute/path/to/my-project' --download-bundle '/absolute/path/to/downloads'
```

已有解压包时，在**解压包根目录**运行包内入口：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\install.ps1 -Project 'C:\work\my-project'
```

```sh
sh installer/install.sh '/absolute/path/to/my-project'
```

已记录的 Python 安装入口也接受 `--bundle-root 解压目录`。这些入口共用同一差分安装流程和内容缓存。

Windows/Linux x64 的 Math 包随完整资源提供；macOS 的 Math DMG 需要首次单独联网获取，未嵌入完整 bundle。因此，在全新 macOS 上准备完整环境仍需该次网络下载。

## 平台前提

- Windows：提供 AMD64 / x64 资源。
- Linux / WSL：x64 提供核心和 Math 资源；项目使用区分大小写的文件系统。WSL 可选择 Linux 用户目录下的独立项目目录。
- macOS：13 或更高版本，分别提供 Apple Silicon 与 Intel 的资源路线。
- Linux ARM64：已有核心资源，尚缺完整 Math 包；当前完整安装会在登记主 skill 前停止并说明原因。

平台表描述资源供给，不代表本版本已经逐平台实机验证。参见[版本与证据说明](release-status.md)。

## 查看安装结果

程序返回简短摘要，并将详细记录保存在项目 `.lotraAI-build` 中。主要入口与回执：

| 文件 | 用途 |
| --- | --- |
| `install-entry/Launcher.json` | 后续安装、更新和完整包下载入口 |
| `Active-skill.json` | 当前选中的 skill |
| `Bundle-install.json` | 实际准备的运行资源与能力事实 |

`core_ready`、`render_ready`、`native_edit_ready` 与具体原图的整图验收分别记录。安装完成不能替代某次 PPT 重建的质量验收。

交给 Codex 执行时，优先读取入口和摘要；只有出现具体错误时再读取对应日志，避免把完整清单、缓存目录和全部日志展开到对话中。
