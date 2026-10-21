# MSF — My Skill Folder

简体中文 | [English](README.md)

MSF 是一套轻量、显式调用的 Claude Code 工作流，用于在多个独立任务之间保存项目规划，并按照已确认的计划进行可靠执行。

它包含四个技能：

- `/msf-init`：在项目内创建并说明 `.msf/` 工作区。
- `/msf-plan`：调查项目、检查需求覆盖情况并生成可审批的计划，不修改业务文件。
- `/msf-action`：在新的会话中审查并执行指定计划，自动把可恢复上下文 checkpoint 写入 `.msf`，记录进度并验证结果。
- `/msf-auto`：在一个主任务中完成规划、审批、派发全新上下文的 Action 子 Agent、监督纠偏和最终验收，但不让规划与执行 Agent 共用上下文或同时写代码。

这些技能不会自动触发，必须由用户明确调用。

## 让 Claude Code 帮你安装

把下面这段话直接发送给 Claude Code：

```text
请帮我安装这个 GitHub 仓库里的 MSF 技能：
https://github.com/DnepsMas/MSF

请先检查 README、scripts/install.py 和四个 skills/*/SKILL.md，确认安装内容安全；然后克隆仓库并运行安装脚本，将 msf-init、msf-plan、msf-action、msf-auto 安装到当前用户的 Claude Code 技能目录（~/.claude/skills）。安装后验证四个技能都存在，并告诉我如何开始使用。如果已经安装旧版本，请使用 --force 更新。
```

Claude Code 可能会请求网络访问、写入用户技能目录或运行安装脚本的权限。确认目标确实是本仓库和你的个人技能目录后，再批准这些请求。

安装完成后，Claude Code 通常会自动发现新技能。如果输入 `/msf` 看不到它们，请重启 Claude Code。

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

默认安装位置是当前用户的 `~/.claude/skills`，不会修改你的项目代码。如只想在单个仓库使用，可把 `msf-*` 目录复制到该项目的 `.claude/skills/`。在 WSL 中，`~` 指 WSL 主目录而非 Windows 用户目录。

## 更新已有安装

进入之前克隆的 MSF 仓库，然后执行：

```powershell
git pull
python scripts/install.py --force
```

macOS 或 Linux 可将 `python` 换成 `python3`。

## 验证安装

在 Claude Code 中输入 `/msf`，应能看到：

- `msf-init`
- `msf-plan`
- `msf-action`
- `msf-auto`

也可以先预览安装目标，不写入任何文件：

```powershell
python scripts/install.py --dry-run
```

## 开始使用

建议在同一个项目中分三个独立的会话（新终端或 `/clear`）使用：

1. 初始化：明确调用 `/msf-init`。
2. 制订计划：新建会话并调用 `/msf-plan`。
3. 执行计划：再新建会话，调用 `/msf-action`，同时提供要执行的 `.msf/plan/*.ai.md` 文件的准确路径。

也可以调用 `/msf-auto` 并指定规划强度，在同一个主任务里完成规划、审批和监督执行。批准计划后，Auto 通过 `Agent` 工具创建无聊天历史继承的 Action 子 Agent（不会 fork 主会话），默认使用宿主默认模型，除非用户指定；指定的模型必须与 `Agent` 工具接受的值完全一致，否则 Auto 会列出最多三个相近候选并等待确认，不会静默纠正或降级。主 Agent 等待完成通知，用 `SendMessage` 反馈纠偏并独立验收，不直接修改业务文件，也不把启动命令转交给用户。监督被中断后，可使用 `/msf-auto resume <准确的 .ai.md 路径>` 恢复。

MSF 默认使用中文回复。规划与执行分开，能让你先审阅方案，再授权 Claude Code 修改项目。

执行期间，`/msf-action` 会在首次修改代码前建立 checkpoint，并在任务状态变化、验证完成、等待外部输入、准备切换模型或任务、收到中断信号以及收尾时更新它。切换模型、额度耗尽、Claude Code 崩溃或主动新开任务后，只需再次调用 `/msf-action` 并提供同一份计划的准确路径；它会从 `.msf/memory/sessions/` 和对应开发日志恢复，并先与当前工作区核对，不依赖旧聊天记录。

突发崩溃仍可能丢失最后一次 checkpoint 之后的上下文，因此恢复时不会直接信任未记录的文件变化，而会把它们标记为未验证进度并重新核对。

## 开发校验

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
```

## 许可证

[MIT](LICENSE)
