# Chat object with a terse system prompt.
# Not sourced at quarto render time.

library(ellmer)

chat <- chat_anthropic(
  system_prompt = "Be terse. Prefer R examples."
)
chat$chat("Who are you?")
