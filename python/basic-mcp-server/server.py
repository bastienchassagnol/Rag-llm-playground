"""Tiny FastMCP server for the course (stdio)."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("course-demo")


@mcp.tool()
def hello(name: str = "world") -> str:
    """Return a short greeting. Useful as a smoke test for the host."""
    return f"Hello, {name}."


@mcp.tool()
def pwd() -> str:
    """Return the server process working directory."""
    return str(Path.cwd())


if __name__ == "__main__":
    mcp.run()
