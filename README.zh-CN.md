# lotraAI 完整包下载

[English](README.md) · [简体中文](README.zh-CN.md)

本仓库分发 lotraAI 完整 bundle，维护版本绑定与下载清单。产品介绍、案例和 skill 源码位于[主项目](https://github.com/jiang-zl/lotraAI-image2slide-skill)。

## 当前版本：v1.31.0


完整文件为 `lotraAI-image2slide-v1.31.0-bundle.zip`，大小 2,414,649,382 字节，包含 skill 与全部随包运行资源。SHA-256 为 `200f65a42b96dca2a0143f43f1c3583d5150958ae1fc7ac8c6dea41969fbe657`。

## 下载并合并

打开 [v1.31.0 完整包 Release](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/tag/v1.31.0)。两个 `.part001` / `.part002` 附件是同一个完整 ZIP 按顺序切出的字节分块。保存 Release 中的[下载合并程序](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/download/v1.31.0/fetch_bundle.py)，执行：

~~~sh
python3 fetch_bundle.py --output-dir ./downloads
~~~

Windows 对应命令为 `py fetch_bundle.py --output-dir .\downloads`。程序获取[版本清单](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/download/v1.31.0/v1.31.0.json)，逐块检查，合并 ZIP，并验证整包 SHA-256 后才生成正式输出文件。已有的不同文件会被保留。

也可以把 [Release 地址](https://github.com/jiang-zl/lotraAI-image2slide-skill-runtime/releases/tag/v1.31.0) 直接交给 Codex，要求它按清单和下载程序获取完整包，再解压安装。已经合并好的完整 ZIP 仍可直接交给 Codex。

合并后的唯一交付归档为 `lotraAI-image2slide-v1.31.0-bundle.zip`，内部文件与载荷不因分块传输发生变化。分块大小遵循 [GitHub 单附件限制](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases#storage-and-bandwidth-quotas)。

## 快速开始

### 1. 将完整 bundle 交给 Codex

下载 `lotraAI-image2slide-v1.31.0-bundle.zip`。完整包已包含 skill 和 runtime 资源（Python、依赖、OCR 和 Math）。将 ZIP 放到 Codex 可访问的当前项目目录，或在对话中提供它的本地绝对路径，无需提前手动解压。

### 2. 发送安装请求

把下面的提示词发送给 Codex：

~~~bash
帮我解压提供的完整包 lotraAI-image2slide-v1.31.0-bundle.zip，
使用包内安装器，将其中的 skill 安装到当前项目，命名为 lotra-image2slide-skill。
请先准备包内的 runtime 资源（Python、依赖、OCR 和 Math），再登记主 skill。
完成后告诉我 skill 入口和运行时准备情况。
~~~

Codex 按当前平台调用包内安装器，先准备项目内运行时，再登记唯一的 `lotra-image2slide-skill`。运行资源和私有任务状态位于项目 `.lotraAI-build`。

安装完成后，在同一项目附上参考图，并要求使用 `$lotra-image2slide-skill` 开始重建。手动安装命令见主项目 `lotraAI` 的安装文档。

[完整包组成](docs/bundle-contents.md) · [v1.31.0 版本清单](releases/v1.31.0.json) · [来源与许可](NOTICE.md) · [发布准备](docs/publication-checklist.md)
