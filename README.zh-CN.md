# lotraAI 完整包与运行资源


<!-- workflow-v137:start -->
1.37.1 仍是可移植的 skill：通过项目内 `start → next → submit` 工作包、分批原图观察/绑定、
完整质量验收和正式导出重建 PPT。分批检查点不代表通过；原生构建稿不代表成品。
交付前运行 `delivery-check` 验证当前任务和最终 PPTX 字节。无需更换 harness、
常驻服务或额外模型密钥。可选检查脚本仅供接入方调用，skill 不控制第三方回复。
<!-- workflow-v137:end -->

优先使用通过实际能力检查的本地 PowerPoint／WPS，LibreOffice 作为可选回退。最终文件执行真实导出与保存检查；保存目录可自选，默认项目目录。复用 runtime 1.14.0 二进制；WPS／macOS 必须由对应实机资格检查确认。



**当前产品发布版本：1.37.1** · 开发／默认分支：`dev` · 版本分支：`1.37.1`

两个分支当前均服务于产品 1.37.1。Runtime 二进制仍为 1.14.0，未变化的平台资源继续复用既有 `v1.34.0` 资源发布。产品正式标签为 [`v1.37.1`](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/tag/v1.37.1)。分支使用 `dev` 或 `X.Y.Z`，标签使用 `vX.Y.Z`，不增加其他后缀。

[English](README.md) · [简体中文](README.zh-CN.md)

本仓库分发 lotraAI 完整 bundle 与平台运行资源，维护自动安装、差分更新和下载清单。产品介绍、案例和 skill 源码位于[主项目](https://github.com/jiang-zl/lotraAI-image2slide-skill/blob/dev/README.zh-CN.md)。

## 当前完整包：1.37.1

完整文件为 `lotraAI-image2slide-v1.37.1-bundle.zip`，包含 skill 与当前随包运行资源。大小、SHA-256 和分块顺序以[完整包清单](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/download/v1.37.1/v1.37.1-bundle.json)为准。

运行资源覆盖 Windows x64、Linux x64、macOS Apple Silicon 和 Intel。macOS 要求 13 或更高版本，Math DMG 首次单独联网获取，未包含在完整 bundle 中；Linux ARM64 有核心资源，尚缺完整 Math 包。详见[安装说明](docs/installation.zh-CN.md)。

## 快速开始

### 1. 让 Codex 安装或更新

在工作项目中发送这一句话即可，无需先手动下载完整包：

~~~text
请从 https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime 在当前项目安装或更新 lotraAI Image2Slide。
~~~

Codex 按当前平台调用维护好的安装入口，先准备项目内运行资源，再登记唯一的 `lotra-image2slide-skill`。下载、续传、校验与分块合并由程序完成。已有安装优先复用项目 `.lotraAI-build/install-entry/Launcher.json` 中记录的入口；首次入口见[安装说明](docs/installation.zh-CN.md)。

如果已有完整 ZIP，提供文件或本地绝对路径，发送：

~~~text
请用提供的 lotraAI-image2slide-v1.37.1-bundle.zip 在当前项目安装或更新 Image2Slide。
~~~

### 2. 附上原图开始重建

~~~text
用 $lotra-image2slide-skill 将这张图重建为可编辑 PPT。
~~~

运行资源和私有任务状态位于项目 `.lotraAI-build`。使用方法和案例见[主项目](https://github.com/jiang-zl/lotraAI-image2slide-skill/blob/dev/README.zh-CN.md)。

## 按系统下载安装

也可以先进入要使用 Image2Slide 的项目目录，直接执行对应命令。脚本会自动选择当前系统和架构，首次安装与后续更新使用同一入口。

**Windows（PowerShell）**

```powershell
$url = 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.ps1'
curl.exe -fL --retry 2 --connect-timeout 20 $url -o install-lotra.ps1
if ($LASTEXITCODE -eq 7) { curl.exe --noproxy '*' -fL --retry 2 --connect-timeout 20 $url -o install-lotra.ps1 }
if ($LASTEXITCODE -eq 0) { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-lotra.ps1 -Project (Get-Location).Path }
```

**macOS（终端，Apple Silicon / Intel）**

```sh
curl -fL --retry 2 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.sh' -o install-lotra.sh && sh install-lotra.sh "$PWD"
```

**Linux / WSL（终端）**

```sh
curl -fL --retry 2 'https://raw.githubusercontent.com/jiang-zl/lotraAI-image2slide-skill/dev/install-lotra.sh' -o install-lotra.sh && sh install-lotra.sh "$PWD"
```

skill 包内也提供 `scripts/install-runtime.ps1` 和 `scripts/install-runtime.sh`，可为指定项目补齐或更新 runtime。各入口共用安装核心，使用相同的资源校验、缓存与差分同步流程。参数和已有解压包的用法见安装说明。

## 下载并合并

需要保存完整包时，把本仓库地址交给 Codex，再发送：

~~~text
下载 lotraAI Image2Slide 的完整安装包到当前项目。
~~~

[1.37.1 完整包 Release](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/tag/v1.37.1) 的 19 个分块（`.part001` 至 `.part019`，每块不超过 128 MiB）是同一个 ZIP 按顺序切出的字节片段。程序按清单下载、逐块校验、合并并核对整包 SHA-256，完成后才生成正式 ZIP。中断后保留可续传的下载进度。

下载和安装共用程序与内容缓存。已有解压包也可直接通过包内安装器进入同一安装流程；具体命令见[完整包与本地安装](docs/installation.zh-CN.md#完整包与本地安装)。

## 差分更新

更新仍使用快速开始中的同一句话。新版新增的文件加入、变化的文件替换、新版移除的受管理文件删除；未变化的生效文件不重复下载或写入。文件改名但内容相同时，优先复用本地已有内容，日常更新无需重新获取完整包。

个人知识库、字体、任务、原图、PPT 和全局技能保留。用户自行改动过或归属不明的文件会保留并报告冲突，更新只清理有归属的受管理文件。

[安装说明](docs/installation.zh-CN.md) · [1.37.1 安装清单](https://github.com/jiang-zl/lotraAI-image2slide-skill/releases/download/v1.37.1/release.json) · [来源与许可](NOTICE.md) · [版本与证据说明](docs/release-status.md)

## 本地软件与保存目录

后端必须通过真实 PDF 导出、编辑、保存、重开检查，程序存在不等于可用。Windows PowerPoint 已由测试主机验证；WPS 与 macOS PowerPoint 适配器需要对应主机的实际资格检查。公式保持可编辑 OMML。LibreOffice 回退使用任务自有 TEMP／配置目录，PNG 预览不计为 PDF 导出成功。

可以直接告诉 Agent“保存到 DIRECTORY”，默认保存根目录为当前项目。每次导出建立 `output-slide-YYYY-MM-DD-HHMMSS-mmm`，只交付 `Final_editable.pptx` 和 `Report.md`；任务、探测与日志留在 `.lotraAI-build`。通过项目启动器运行 `presentation-backend --project PROJECT` 检查能力，`presentation-backend --project PROJECT --backend powerpoint --save-preferences` 保存偏好，`export TASK --output-root DIRECTORY` 指定目录，`validate-presentation FILE --project PROJECT --out NEW_AUDIT_DIRECTORY` 检查副本。明确指定的后端不可用时报告具体原因。保留已有文件。
