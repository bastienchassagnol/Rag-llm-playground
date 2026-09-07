"""Anthropic Messages API with two teaching tools: today and multiply."""

from __future__ import annotations

from datetime import date

from anthropic import Anthropic

TOOLS = [
    {
        "name": "today",
        "description": "Return today's date in ISO format.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers exactly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
        },
    },
]


def run_tool(name: str, args: dict) -> str:
    if name == "today":
        return date.today().isoformat()
    if name == "multiply":
        return str(args["a"] * args["b"])
    raise ValueError(f"unknown tool: {name}")


def chat_with_tools(prompt: str) -> str:
    client = Anthropic()
    messages: list[dict] = [{"role": "user", "content": prompt}]
    while True:
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            output = run_tool(block.name, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )
        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print(chat_with_tools("What day is it today?"))
    print(chat_with_tools("What is 384729 * 918273?"))
