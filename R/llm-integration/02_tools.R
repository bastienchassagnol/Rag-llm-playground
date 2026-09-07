# Register clock and calculator tools, then ask one combined question.
# Not sourced at quarto render time.

library(ellmer)

chat <- chat_anthropic()
chat$register_tool(tool(
  fun = function() as.character(Sys.Date()),
  name = "today",
  description = "Return today's date (ISO)."
))
chat$register_tool(tool(
  fun = function(a, b) a * b,
  name = "multiply",
  description = "Multiply two numbers exactly.",
  arguments = list(
    a = type_number(),
    b = type_number()
  )
))
chat$chat("What day is it? What is 384729 * 918273?")
