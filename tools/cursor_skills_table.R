# Build grouped tinytable for tools/chatgpt-companions.qmd (tbl-cursor-skills).
# Requires tinytable (install.packages if missing).
build_cursor_skills_table <- function(
    csv_path = "tools/data/cursor_skills_inventory.csv"
) {
  if (!requireNamespace("tinytable", quietly = TRUE)) {
    stop(
      "Package 'tinytable' is required. ",
      "Install with install.packages('tinytable').",
      call. = FALSE
    )
  }
  path <- csv_path
  if (!file.exists(path) && file.exists(file.path("..", csv_path))) {
    path <- file.path("..", csv_path)
  }
  d <- read.csv(path, stringsAsFactors = FALSE)
  d <- d[order(d$family, d$skill), ]
  rle <- rle(d$family)
  starts <- cumsum(c(1L, head(rle$lengths, -1L)))
  idx <- setNames(as.list(starts), rle$values)
  tab <- tinytable::tt(d[, c("skill", "role")])
  tinytable::group_tt(tab, i = idx)
}
