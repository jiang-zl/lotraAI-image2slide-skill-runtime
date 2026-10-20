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

完整包由清单规定的 19 个有序分块组成，下载程序负责续传、逐块校验、合并与整包校验。需要先下载到指定位置时，可使用：

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

## macOS 公式后端（1.35.3）

由保留原签名的 LibreOffice 主应用，在新建的项目私有配置中执行固定 Python／UNO 工作器；安装器不直接启动受父进程约束的内嵌解释器。应用签名与系统安全设置保持原样。安装启动检查与正式导出使用同一工作器，每次安装尝试都进行新的原生 Math 启动检查。

如果此前只安装了技能文件，在同一项目重新运行维护安装入口即可继续准备；已验证资源保留。诊断以本次 `Failure.json`、`Math-backend-failure.json` 及其引用的 `backend-result.json` 为准，记录阶段、命令、退出状态和日志路径。尚未到达的核心阶段标记为 `NOT_RUN`。启动检查成功不代表实际文档渲染或整图质量验收。

GitHub Release 下载增加有限次数的官方资产 API 备用通道，仍校验相同的大小、SHA-256、范围响应和缓存归属。macOS Math DMG 继续使用固定的上游地址。Apple Silicon 与 Intel 的 macOS 实机检查仍待完成，Windows 结果不作为两种 Mac 架构的通过证据。

## 1.35.5 安装入口

所有 shell 安装入口使用无 BOM 的 UTF-8 与 LF。维护者从固定模板生成入口，并对最终附件、skill ZIP 和完整包中的实际脚本执行解析检查。Windows 入口同时检查 Windows PowerShell 解析与真实安装。runtime 二进制与资源包保持不变。
