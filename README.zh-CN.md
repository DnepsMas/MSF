# MSF — My Skill Folder

简体中文 | [English](README.md)

MSF 是一套轻量、显式调用的 Codex 工作流，用于在多个独立任务之间保存项目规划，并按照已确认的计划进行可靠执行。

它包含三个技能：

- `$msf-init`：在项目内创建并说明 `.msf/` 工作区。
- `$msf-plan`：调查项目、检查需求覆盖情况并生成可审批的计划，不修改业务文件。
- `$msf-action`：在新的 Codex 任务中审查并执行指定计划，记录进度并验证结果。

这些技能不会自动触发，必须由用户明确调用。

## 让 Codex 帮你安装

把下面这段话直接发送给 Codex：

```text
请帮我安装这个 GitHub 仓库里的 MSF 技能：
https://github.com/DnepsMas/MSF

请先检查 README、scripts/install.py 和三个 skills/*/SKILL.md，确认安装内容安全；然后克隆仓库并运行安装脚本，将 msf-init、msf-plan、msf-action 安装到当前用户的 Codex 技能目录。安装后验证三个技能都存在，并告诉我如何开始使用。如果已经安装旧版本，请使用 --force 更新。
```

Codex 可能会请求网络访问、写入用户技能目录或运行安装脚本的权限。确认目标确实是本仓库和你的个人技能目录后，再批准这些请求。

安装完成后，Codex 通常会自动发现新技能。如果 `/skills` 中没有出现它们，请重启 Codex。

## 手动安装

需要安装 Git 和 Python 3。

Windows PowerShell：

```powershell
git clone https://github.com/DnepsMas/MSF.git
cd MSF
python scripts/install.py
```

macOS 或 Linux：

```bash
git clone https://github.com/DnepsMas/MSF.git
cd MSF
python3 scripts/install.py
```

默认安装位置是当前用户的 `~/.agents/skills`，不会修改你的项目代码。

## 更新已有安装

进入之前克隆的 MSF 仓库，然后执行：

```powershell
git pull
python scripts/install.py --force
```

如果以前曾将 MSF 安装到 `~/.codex/skills`，请执行迁移，避免 `/skills` 或技能选择菜单出现重复项：

```powershell
python scripts/install.py --force --remove-legacy
```

安装器检测到旧位置仍有同名技能时会停止并给出提示，不会静默安装第二份。`--remove-legacy` 只会在新版本安装成功后移除旧位置中的三个 `msf-*` 目录。

macOS 或 Linux 可将 `python` 换成 `python3`。

## 验证安装

在 Codex 中运行 `/skills`，应能看到：

- `msf-init`
- `msf-plan`
- `msf-action`

也可以先预览安装目标，不写入任何文件：

```powershell
python scripts/install.py --dry-run
```

## 开始使用

建议在同一个项目中分三个独立的 Codex 任务使用：

1. 初始化：明确调用 `$msf-init`。
2. 制订计划：新建任务并调用 `$msf-plan`。
3. 执行计划：再新建任务，调用 `$msf-action`，同时提供要执行的 `.msf/plan/*.ai.md` 文件的准确路径。

MSF 默认使用中文回复。规划与执行分开，能让你先审阅方案，再授权 Codex 修改项目。

## 开发校验

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
```

## 许可证

[MIT](LICENSE)
