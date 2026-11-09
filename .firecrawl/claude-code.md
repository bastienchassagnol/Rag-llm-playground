# Claude Code Cheat Sheet for Python Developers [Permanent link](https://realpython.com/cheatsheets/claude-code/\#claude-code-cheat-sheet-for-python-developers "Permanent link")

This Claude Code cheat sheet for Python developers condenses the commands, shortcuts, and config files you reach for every day: CLI flags and headless mode, slash commands, keyboard shortcuts, CLAUDE.md, permissions, settings, hooks, skills, subagents, and MCP servers. Every command matches the official Claude Code documentation, so you can keep this Claude cheat sheet open next to your terminal while you work.

You can also download the information as a printable cheat sheet:

Free Bonus: **Claude Code Cheat Sheet**

Get a **Claude Code Cheat Sheet (PDF)** with slash commands, shortcuts, CLI flags, CLAUDE.md, permissions, hooks, skills, subagents, and MCP on two printable pages:

![Claude Code Cheat Sheet](https://files.realpython.com/media/claude-code-cheat-sheet-stacked.614668b569fb.png)

Send My Claude Code Cheat Sheet »

Practice with hands-on [coding exercises](https://realpython.com/coding-exercises/), [quizzes](https://realpython.com/quizzes/), and a [personal AI mentor](https://realpython.com/mentor/). Not sure what to learn next? Get your [free personal learning plan](https://realpython.com/account/learning-plan/).

New to Claude Code?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Help me figure out where to start

## Install and Start [Permanent link](https://realpython.com/cheatsheets/claude-code/\#install-and-start "Permanent link")

- Start `claude` in your project root and avoid your home folder.
- Sign in with a paid Claude plan or an Anthropic Console account.
- Type `/` for commands and `?` for shortcuts.

Language: ShellFilename: `Install on macOS and Linux`

```
$ curl -fsSL https://claude.ai/install.sh \
    | bash
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: Windows PowerShellFilename: `Install on Windows`

```
PS> irm https://claude.ai/install.ps1 | iex
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Check and Update`

```
$ claude --version
$ claude update
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Start a Session`

```
$ cd my-project/
$ claude                      # Interactive
$ claude "explain this repo"  # With prompt
$ claude -n auth-fix          # Named
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Resume a Session`

```
$ claude -c          # Latest one in this dir
$ claude -r          # Pick from a list
$ claude -r auth-fix "finish the PR"
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Launch Flags`

```
$ claude --model sonnet
$ claude --effort high
$ claude --permission-mode plan
$ claude --add-dir ../shared-lib
$ claude -w feature-x   # In a git worktree
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Walk through a full project in [How to Use Claude Code to Write and Debug Python](https://realpython.com/how-to-use-claude-code/).

Want a guided first session?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me where to learn Claude Code basics

## Run Claude Code Headless [Permanent link](https://realpython.com/cheatsheets/claude-code/\#run-claude-code-headless "Permanent link")

- `-p` prints one answer and exits, so it fits scripts and CI.
- `--allowedTools` pre-approves the tools a script needs.
- `--bare` skips CLAUDE.md, hooks, skills, and MCP for faster starts.

Language: ShellFilename: `One-Shot Prompts`

```
$ claude -p "explain this function"
$ cat error.log | claude -p "root cause?"
$ claude -c -p "check for type errors"
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `JSON Output and Limits`

```
$ claude -p "summarize this project" \
    --output-format json | jq -r '.result'
$ claude -p "fix the failing test" \
    --allowedTools "Read,Edit,Bash" \
    --max-turns 5
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Scripting Claude Code?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Help me run Claude Code in CI

## Session Slash Commands [Permanent link](https://realpython.com/cheatsheets/claude-code/\#session-slash-commands "Permanent link")

- Type `/` to list commands, then keep typing to filter.
- Put the command at the start of your message.
- Run `/clear` when you switch tasks and `/compact` to keep going.

### Context [Permanent link](https://realpython.com/cheatsheets/claude-code/\#context "Permanent link")

| Command | What it does |
| --- | --- |
| `/context` | Show context usage |
| `/compact [focus]` | Summarize the chat to free space |
| `/clear` | Start a fresh chat. Also `/new` |
| `/btw [question]` | Ask a side question |

### Sessions [Permanent link](https://realpython.com/cheatsheets/claude-code/\#sessions "Permanent link")

| Command | What it does |
| --- | --- |
| `/resume [name]` | Reopen a session. Also `/continue` |
| `/rename [name]` | Label this session |
| `/branch [name]` | Try another direction |
| `/rewind` | Roll back code and chat. Also `/undo` |
| `/export [file]` | Save the chat as plain text |
| `/exit` | Quit. Also `/quit` |

### Background Work [Permanent link](https://realpython.com/cheatsheets/claude-code/\#background-work "Permanent link")

| Command | What it does |
| --- | --- |
| `/tasks` | List running shells and agents |
| `/subtask <task>` | Hand a task to a forked subagent |
| `/fork [prompt]` | Run a copy in the background |
| `/background` | Detach the session. Also `/bg` |
| `/goal [condition]` | Keep working until the goal is met |
| `/loop 5m <prompt>` | Repeat a prompt on an interval |

Not sure which one to use?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Help me choose between /fork, /subtask, and /background

## Setup and Review Slash Commands [Permanent link](https://realpython.com/cheatsheets/claude-code/\#setup-and-review-slash-commands "Permanent link")

- Press `s` in the `/model` picker to switch for this session only.
- Raise `/effort` for hard problems, at the cost of more tokens.

### Model and Usage [Permanent link](https://realpython.com/cheatsheets/claude-code/\#model-and-usage "Permanent link")

| Command | What it does |
| --- | --- |
| `/model [name]` | Switch model and save it as default |
| `/effort high` | Set effort from low to max, or auto |
| `/fast` | Toggle fast mode, or pass `on` or `off` |
| `/usage` | Show cost and limits. Also `/cost` |

### Configure [Permanent link](https://realpython.com/cheatsheets/claude-code/\#configure "Permanent link")

| Command | What it does |
| --- | --- |
| `/config` | Open settings. Also `/settings` |
| `/config theme=dark` | Set one key directly |
| `/permissions` | Edit allow, ask, and deny rules |
| `/memory` | Edit memory files |
| `/hooks` | View configured hooks |
| `/skills` | List and toggle skills |
| `/mcp` | Manage MCP servers and OAuth |
| `/doctor` | Diagnose your setup |
| `/status` | Show version and account |

### Plan and Review [Permanent link](https://realpython.com/cheatsheets/claude-code/\#plan-and-review "Permanent link")

| Command | What it does |
| --- | --- |
| `/init` | Draft a CLAUDE.md |
| `/plan [task]` | Enter plan mode |
| `/diff` | Review the working tree |
| `/code-review --fix` | Find and fix bugs |
| `/code-review ultra` | Run a deep cloud review |
| `/security-review` | Find security issues |
| `/simplify` | Clean up the code |

Plan first, then edit?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me how plan mode fits my workflow

**Free Bonus:** [Download the Claude Code Cheat Sheet PDF](https://realpython.com/bonus/claude-code-cheat-sheet-inline/) and keep the essentials at hand.

## More Slash Commands [Permanent link](https://realpython.com/cheatsheets/claude-code/\#more-slash-commands "Permanent link")

- Your skills and plugin skills share the same `/` menu.
- MCP server prompts show up as `/server:prompt`.

### Workspace [Permanent link](https://realpython.com/cheatsheets/claude-code/\#workspace "Permanent link")

| Command | What it does |
| --- | --- |
| `/add-dir <path>` | Grant access to another directory |
| `/cd <path>` | Move the session and keep the chat |
| `/ide` | Connect your IDE |
| `/copy [N]` | Copy a response |
| `/insights` | Report on your sessions |

### Look and Feel [Permanent link](https://realpython.com/cheatsheets/claude-code/\#look-and-feel "Permanent link")

| Command | What it does |
| --- | --- |
| `/theme` | Pick a color theme |
| `/color [color]` | Set the prompt bar color |
| `/statusline` | Configure the status line |
| `/keybindings` | Edit the shortcuts file |
| `/help` | List all commands |
| `/release-notes` | See what’s new |

### Extend [Permanent link](https://realpython.com/cheatsheets/claude-code/\#extend "Permanent link")

| Command | What it does |
| --- | --- |
| `/plugin` | Browse and install plugins |
| `/reload-skills` | Pick up new skills |
| `/workflows` | Watch dynamic workflows |
| `/schedule` | Set up recurring cloud routines |

Want to extend Claude Code?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me where to learn about plugins

## Keyboard Shortcuts [Permanent link](https://realpython.com/cheatsheets/claude-code/\#keyboard-shortcuts "Permanent link")

- On macOS, press `Option` for `Alt`. Most of these need Option set as Meta, but `Option+T` works without it.

### Control the Session [Permanent link](https://realpython.com/cheatsheets/claude-code/\#control-the-session "Permanent link")

| Keys | Action |
| --- | --- |
| `Shift+Tab` | Cycle permission modes |
| `Esc` | Interrupt Claude |
| `Esc``Esc` | Clear input or rewind |
| `Ctrl+C` | Interrupt, clear, or exit when pressed twice |
| `Ctrl+O` | Toggle transcript viewer |
| `Ctrl+B` | Background a running task |
| `Ctrl+T` | Toggle the task checklist |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle extended thinking |
| `Alt+O` | Toggle fast mode |
| `Ctrl+L` | Redraw the screen |

### Write Your Prompt [Permanent link](https://realpython.com/cheatsheets/claude-code/\#write-your-prompt "Permanent link")

| Keys | Action |
| --- | --- |
| `\``Enter`, `Ctrl+J` | New line |
| `Shift+Enter` | New line in most terminals |
| `Ctrl+R` | Search prompt history |
| `Ctrl+G` | Edit prompt in your editor |
| `Ctrl+S` | Stash or restore the prompt |
| `Ctrl+V` | Paste an image |
| `Cmd+V` | Paste an image in iTerm2 |
| `Alt+V` | Paste an image on Windows or WSL |
| `!` at start | Shell mode |
| `@` | Mention a file or subagent |
| `?` | Show all shortcuts |

Curious about @ and !?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me what these prompt tricks do

## CLAUDE.md and Memory [Permanent link](https://realpython.com/cheatsheets/claude-code/\#claudemd-and-memory "Permanent link")

- CLAUDE.md holds instructions you write. Auto memory holds notes Claude writes.
- All files load together from broad to specific, so remove contradictions.
- Since v2.1.277, `AGENTS.md` loads when a repo has no CLAUDE.md.

### Where CLAUDE.md Files Live [Permanent link](https://realpython.com/cheatsheets/claude-code/\#where-claudemd-files-live "Permanent link")

| File | Scope |
| --- | --- |
| `~/.claude/CLAUDE.md` | You, in every project |
| `./CLAUDE.md` | Your team. Commit it |
| `./CLAUDE.local.md` | You, in this project |
| `sub/CLAUDE.md` | Loads on demand |

Language: Markdown TextFilename: `Import Files`

```
# Project Notes
See @README.md for an overview.
- Testing: @docs/testing.md
- Mine: @~/.claude/my-notes.md
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: Markdown TextFilename: `Scope a Rule in .claude/rules/api.md`

```
---
paths:
  - "src/api/**/*.py"
---
- Validate every request body
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Set up global, project, and local files in [How to Write a CLAUDE.md File for Claude Code](https://realpython.com/python-claude-md/).

Starting a CLAUDE.md?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Help me write my first CLAUDE.md

## Permissions and Modes [Permanent link](https://realpython.com/cheatsheets/claude-code/\#permissions-and-modes "Permanent link")

- `Shift+Tab` cycles `default`, `acceptEdits`, and `plan`, plus `auto` when it’s available.
- Since v2.1.283, most terminal and VS Code sessions start in `auto`.
- The UI labels `default` mode as Manual.
- Rules check deny, then ask, then allow. The first match wins.
- Deny rules hold in every mode, even `bypassPermissions`.

| Mode | Runs without asking |
| --- | --- |
| `default` | Reads only |
| `acceptEdits` | Reads, edits, file commands |
| `plan` | Reads to draft a plan |
| `auto` | Everything, with safety checks |
| `dontAsk` | Pre-approved tools and file reads |
| `bypassPermissions` | Everything, in isolated VMs |

Language: JSONFilename: `Permission Rules`

```
{
  "permissions": {
    "allow": ["Bash(uv run pytest *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)"]
  }
}
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Still fuzzy on permission rules?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Explain permission rules another way

**Free Bonus:** [Download the Claude Code Cheat Sheet PDF](https://realpython.com/bonus/claude-code-cheat-sheet-inline/) and keep the essentials at hand.

## Settings Files [Permanent link](https://realpython.com/cheatsheets/claude-code/\#settings-files "Permanent link")

- Managed settings win, followed by `--settings`, local, project, and user.
- List keys like `permissions.allow` merge across files.
- Settings files are strict JSON with no comments or trailing commas.
- `/status` shows which files loaded.

### Where Settings Live [Permanent link](https://realpython.com/cheatsheets/claude-code/\#where-settings-live "Permanent link")

| File | Scope |
| --- | --- |
| `~/.claude/settings.json` | User |
| `.claude/settings.json` | Project, shared |
| `.claude/settings.local.json` | Project, just you |

Two files, one key?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me what happens when settings conflict

## Hooks [Permanent link](https://realpython.com/cheatsheets/claude-code/\#hooks "Permanent link")

- Hooks run your commands at fixed points in Claude’s loop.
- Exit code 2 from `PreToolUse` blocks the tool call.
- `/hooks` shows what’s registered.

### Key Events [Permanent link](https://realpython.com/cheatsheets/claude-code/\#key-events "Permanent link")

| Event | When it runs |
| --- | --- |
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | Before Claude sees your prompt |
| `PreToolUse` | Before a tool runs. Can block it |
| `PostToolUse` | After a tool succeeds |
| `Notification` | Claude needs your input |
| `Stop` | Claude finished replying |

Language: JSONFilename: `Format After Every Edit`

```
{
  "hooks": {
    "PostToolUse": [{\
      "matcher": "Edit|Write",\
      "hooks": [{\
        "type": "command",\
        "command": "ruff format ."\
      }]\
    }]
  }
}
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Go deeper with these hooks resources:

- [How to Automate Your Workflow With Claude Code Hooks](https://realpython.com/claude-code-hooks/)
- [Claude Code Hooks Cheat Sheet for Python Developers](https://realpython.com/cheatsheets/claude-code-hooks/)

Wondering how the matcher works?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me what this hook does on every edit

## Skills [Permanent link](https://realpython.com/cheatsheets/claude-code/\#skills "Permanent link")

- A folder with a `SKILL.md` becomes a `/name` command.
- Claude also loads a skill when its description fits the task.
- `disable-model-invocation: true` makes a skill manual-only.
- Old `.claude/commands/*.md` files still work.

### Where Skills Live [Permanent link](https://realpython.com/cheatsheets/claude-code/\#where-skills-live "Permanent link")

| File | Scope |
| --- | --- |
| `~/.claude/skills/<name>/SKILL.md` | You |
| `.claude/skills/<name>/SKILL.md` | Project |

Language: Markdown TextFilename: `A Minimal SKILL.md`

```
---
name: docstring-doctor
description: >-
  Writes Google-style Python docstrings.
  Use when asked to document code.
---
Open with a one-line summary...
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Claude follows the instructions below the frontmatter each time the skill runs.

Go deeper with this skills resource:

- [How to Use Claude Code Skills for Better Python Docstrings](https://realpython.com/claude-code-skills/)

Think you’ve got skills down?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Quiz me on skills

## Subagents [Permanent link](https://realpython.com/cheatsheets/claude-code/\#subagents "Permanent link")

- A subagent works in its own context and reports back.
- Built-in subagents include Explore, which searches without editing, and Plan.
- Claude can write one for you, or you can add a file to `.claude/agents/`.

Language: Markdown TextFilename: `Define .claude/agents/code-reviewer.md`

```
---
name: code-reviewer
description: Reviews code for quality
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer...
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Run the Session as an Agent`

```
$ claude --agent code-reviewer
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: TextFilename: `Call a Subagent`

```
@agent-code-reviewer check my changes
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Skill or subagent?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Help me choose between a skill and a subagent

**Free Bonus:** [Download the Claude Code Cheat Sheet PDF](https://realpython.com/bonus/claude-code-cheat-sheet-inline/) and keep the essentials at hand.

## MCP Servers [Permanent link](https://realpython.com/cheatsheets/claude-code/\#mcp-servers "Permanent link")

- MCP connects Claude Code to outside tools and data.
- Scopes are `local`, `project`, and `user`, with `local` as the default.
- Project scope saves servers to a shared `.mcp.json` file.
- For stdio servers, `--` comes before the server command.
- Connect databases with a read-only user.

Language: ShellFilename: `Add a Server`

```
$ claude mcp add --transport http \
    notion https://mcp.notion.com/mcp
$ claude mcp add --transport stdio \
    --scope project db \
    -- npx -y @bytebase/dbhub \
    --dsn "postgresql://readonly:pw@host/db"
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Language: ShellFilename: `Manage Servers`

```
$ claude mcp list
$ claude mcp get notion
$ claude mcp remove notion
```

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)

- ###### ![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Ask Mentor AI

- Pick a question and Mentor AI answers it with this code block in front of it.
- Explain this

- Why is it written this way?

- Walk me through it line by line

- Quiz me on this

- Give me a practice exercise

- * * *

- Ask something else…


Want to go deeper on MCP?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Show me where to learn more about MCP

## Everyday Workflow [Permanent link](https://realpython.com/cheatsheets/claude-code/\#everyday-workflow "Permanent link")

- Switch to plan mode with `Shift+Tab` before big changes.
- Review every diff and commit between tasks.
- Run `/branch` before a risky experiment.
- `/rewind` restores Claude’s file edits but not changes from shell commands.

### A Typical Loop [Permanent link](https://realpython.com/cheatsheets/claude-code/\#a-typical-loop "Permanent link")

| Command | What it does |
| --- | --- |
| `/init` | Once per project |
| `/plan add a CLI` | Agree on a plan |
| `/diff` | Review the edits |
| `/code-review --fix` | Catch bugs early |
| `/clear` | Start the next task |

Ready to test yourself?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Quiz me on the everyday workflow

**Do you want to go deeper on Claude Code?**

Level up your skills with curated resources at Real Python:

- [Coding exercises](https://realpython.com/coding-exercises/)
- [Interactive quizzes](https://realpython.com/quizzes/)
- [Learning paths](https://realpython.com/learning-paths/)
- [Video courses](https://realpython.com/courses/)
- [Written tutorials](https://realpython.com/tutorials/)
- [Reference articles](https://realpython.com/ref/)
- [Podcast interviews](https://realpython.com/podcasts/rpp/)

Become a Python and AI expert with your free personal learning plan at **[realpython.com/learning-plan](https://realpython.com/account/learning-plan/)** 💡🐍

Ready to go beyond the cheat sheet?

![](https://realpython.com/static/mentor/maia.f5d7e1f0f56c.svg)Build me a Claude Code learning plan

You can download this information as a printable cheat sheet:

Free Bonus: **Claude Code Cheat Sheet**

Get a **Claude Code Cheat Sheet (PDF)** with slash commands, shortcuts, CLI flags, CLAUDE.md, permissions, hooks, skills, subagents, and MCP on two printable pages:

![Claude Code Cheat Sheet](https://files.realpython.com/media/claude-code-cheat-sheet-stacked.614668b569fb.png)

Send My Claude Code Cheat Sheet »

Free Bonus: **Python Cheat Sheet** ×

Get a **Python Cheat Sheet (PDF)** and learn the basics of Python, like working with data types, dictionaries, lists, and Python functions:

![Real Python Cheat Sheet showing all three pages stacked on top of each other](https://files.realpython.com/media/cheat_sheets_stacked.34027e654084.png)

Send My Python Cheat Sheet »