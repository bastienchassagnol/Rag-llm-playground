# LLMs, tools, and agents

Quarto **book** (HTML + PDF) for a short course: LLM theory, then
practical work in Python and R.

## Contents

| Part | Path |
|------|------|
| Welcome | `index.qmd` |
| LLM basics | `theory/llm-basics.qmd` |
| MCP vs RAG vs agents | `theory/tools-vs-agents.qmd` |
| Python tool calling | `python/llm-tool-calling.qmd` |
| Minimal MCP server | `python/basic-mcp-server.qmd` |
| R (`ellmer`) | `R/llm-integration.qmd` |
| R versus Python | `R/r-vs-python.qmd` |

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
(`execute.freeze: auto`). Run R, Python, and Mermaid **on your machine**,
then commit `_freeze/` so GitHub Actions can publish without `uv` or
`renv`.

```bash
quarto render     # updates _freeze/ and writes HTML + PDF under docs/
git add -u _freeze
quarto preview
```

Quarto ≥ 1.8; LuaLaTeX (or TinyTeX) for the PDF.

## Attribution

- Architecture diagram in the tools chapter: ByteByteGo,
  *MCP vs RAG vs AI Agents* (`figures/RAGs-vs-AI-agents.jpg`).
- R lab condensed from Hadley Wickham,
  [A no bullshit guide to LLMs](https://tidydesign.substack.com/p/a-no-bullshit-guide-to-llms).
