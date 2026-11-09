# LLMs, tools, and agents

Quarto **website** for a short course: LLM theory, then practical
work in Python and R. Top navigation is one menu per theme. Each
HTML page also has a `.llms.md` twin for agents.

## Contents

| Part | Path |
|------|------|
| Welcome | `index.qmd` |
| LLM basics | `theory/llm-basics.qmd` |
| MCP vs RAG vs agents | `theory/tools-vs-agents.qmd` |
| Pre-existing AI tools | `tools/chatgpt-companions.qmd` |
| Python tool calling | `python/llm-tool-calling.qmd` |
| Minimal MCP server | `python/basic-mcp-server.qmd` |
| Claude Code | `python/claude-code.qmd` |
| Tabular foundation models | `python/tabular-foundation-models.qmd` |
| R (`ellmer`) | `R/llm-integration.qmd` |
| R versus Python | `R/r-vs-python.qmd` |
| Prompt library | `prompts/index.qmd` |

Labs (runnable, not rendered as API calls):

```text
python/basic-mcp-server/
python/llm-tool-calling/
R/llm-integration/
```

## Python labs (`uv`)

From the repository root (do **not** create a second venv inside
`python/`):

```bash
uv sync                          # creates .venv from pyproject.toml + uv.lock
export ANTHROPIC_API_KEY="…"
uv run python python/llm-tool-calling/tool_calling.py
uv run python python/basic-mcp-server/server.py
```

`anthropic` and `mcp` (pinned `<2` so `FastMCP` still imports) are
declared in `pyproject.toml`.

## R lab (`renv`)

```r
# in R, working directory = repository root
renv::restore()
source("R/llm-integration/01_chat.R")
```

`ellmer` 0.5.0 is recorded in `renv.lock`. The project library lives
under `renv/library/` (gitignored).

## Build

Computations use Quarto [freeze](https://quarto.org/docs/publishing/github-pages.html#freezing-computations)
(`execute.freeze: true`). Run R, Python, and Mermaid **on your machine**,
then commit `_freeze/` so GitHub Actions can publish without `uv` or
`renv`.

```bash
quarto render     # updates _freeze/ and writes HTML under docs/
git add -u _freeze
quarto preview
```

Quarto ≥ 1.8. The site is HTML only, so CI does not install TinyTeX.

Search uses [Algolia](https://quarto.org/docs/websites/website-search.html#using-algolia).
After `quarto render`, upload `docs/search.json` to an index named
`rag-llm-playground`, then replace `REPLACE_ME` in `_quarto.yml`
with the application id and the **search-only** API key. Page counts
use [Plausible](https://plausible.io) on
`bastienchassagnol.github.io`; add that hostname in Plausible or the
script runs without a dashboard. LinkedIn unfurls use the Open Graph
tags (`website.open-graph`).

## Attribution

- Architecture diagram in the tools chapter: ByteByteGo,
  *MCP vs RAG vs AI Agents* (`figures/RAGs-vs-AI-agents.jpg`).
- R lab condensed from Hadley Wickham,
  [A no bullshit guide to LLMs](https://tidydesign.substack.com/p/a-no-bullshit-guide-to-llms).
- Tabular foundation models chapter condensed from Christoph Molnar,
  [Tabular Foundation Models](https://tabularfoundationmodels.com/introduction).
