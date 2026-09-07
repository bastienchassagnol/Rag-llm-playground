# ellmer lab

See the book chapter `R/llm-integration.qmd`.

From the **repository root** (project `renv` library):

```r
renv::restore()
source("R/llm-integration/01_chat.R")
source("R/llm-integration/02_tools.R")
```

Set `ANTHROPIC_API_KEY` (or another provider supported by `ellmer`)
before sourcing.
