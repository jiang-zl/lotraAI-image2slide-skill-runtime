# lotraAI runtime 与自动安装

[English](README.md) | **简体中文**

## Quick start

> 请从 https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime 在当前项目安装或更新 lotraAI Image2Slide。

Codex 自动下载并运行正式程序，首次安装和文件差分更新使用同一句话。

## Agent 入口

若已有 `.lotraAI-build/install-entry/Launcher.json`，使用其中记录的安装命令。否则，从本仓库 `release` 分支取得 Windows 的 `tools/install_lotra.ps1` 或 macOS/Linux 的 `tools/install_lotra.sh`，传入项目路径运行。它自动选择平台、按需准备私有 Python、读取 `releases/current.json` 并调用共同安装核心。不要临时重写下载脚本，也不展开完整清单和日志。

## 完整分块包

完整 bundle 保留为每块最多 128 MiB 的有序分块，当前块数和身份由[完整包清单](releases/v1.33.0-bundle.json)记录。程序逐块校验，合并后再核对整包哈希，最后才生成正式 ZIP；重试时保留已校验缓存和有归属的未完成下载。

需要本地安装包或离线副本时，可以直接让 Codex 下载完整 bundle。已有安装入口支持 `--download-bundle 输出目录`；Windows 引导入口对应 `-DownloadBundle 输出目录`，Shell 入口对应 `项目路径 --download-bundle 输出目录`。兼容入口 `tools/fetch_bundle.py --project 项目路径 --output-dir 输出目录` 在准备好的 Python 3.12 下委托同一个程序完成下载。

已有解压包可使用包内 `installer/install.ps1 -Project 项目路径`，或 `sh installer/install.sh 项目路径`。已有 Python 安装入口也支持 `--bundle-root 解压目录`，都进入共同的差分安装流程。macOS 首次准备 Math 时单独联网下载；完整包内保留既有 Windows/Linux Math，不包含 macOS DMG。

## 维护者上传发布

准备好的发布目录提供 `Publish-v1.33.0.ps1`、`Publish-v1.33.0.sh`、`publish_lotra.py` 和精确的 `Publish-plan.json`。程序跳过已上传且匹配的附件，只重试失败分块，全部所需附件齐全后才切换当前版本分支。详见[发布说明](docs/publishing-v133.md)。

首次安装按当前系统和架构选择资源。大资源可以分块下载，由程序自动续传、校验和合并。已有安装按文件清单差分同步：新增新文件、替换变化文件、移除新版已删除的受管理文件；未变化的生效文件不重复下载、不重新写入。文件改名时也优先复用本地相同内容。个人知识库、字体、任务、原图和 PPT 保留在私有 `.lotraAI-build` 中。

完整 bundle 继续提供有序分块，用于本地安装、离线保存和恢复，与正常安装共用正式下载器和内容缓存；日常更新无需下载完整 bundle。参见 [runtime 安装与完整包](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime)。

## 平台与发布范围

产品版本仍为 **1.33.0**。Python/OCR 资源覆盖 Windows AMD64、Linux x86_64/aarch64、macOS Apple Silicon 和 Intel。完整 Math 准备已有 Windows AMD64、Linux x86_64 和两种 macOS 架构的资源路线。macOS 要求 13 或更新版本，需要首次联网取得固定哈希的 Math 磁盘镜像；该镜像未包含在完整 bundle 中。Linux ARM64 有核心资源，尚无随包完整 Math，安装器会明确报告该限制。

本次完成实现与静态代码审查。按用户要求，未运行产品测试、语法/import/CLI 检查、安装、重建/渲染或性能与效果测量。发布哈希用于标识分发内容，不代表运行时或重建质量验收。历史标签与归档保留。

详细流程见[工作流说明](https://github.com/jiang-zl/lotraAI-image2slide-skill/blob/release/skills/lotra-image2slide-skill/references/workflow-v133.md)。
