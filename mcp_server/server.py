"""MCP server exposing healthcare AI documentation as a tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP

from mcp_server.tools import TOOL_DESCRIPTION, TOOL_NAME, handle_query

mcp = FastMCP("MedReg MCP", instructions="Healthcare AI regulatory documentation assistant")


@mcp.tool(name=TOOL_NAME, description=TOOL_DESCRIPTION)
async def query_healthcare_ai_docs(question: str) -> str:
    """Search FDA and WHO documentation about healthcare AI regulation.

    Args:
        question: A question about healthcare AI regulation, responsible AI, or medical device software.
    """
    return await handle_query(question)


if __name__ == "__main__":
    mcp.run(transport="stdio")
