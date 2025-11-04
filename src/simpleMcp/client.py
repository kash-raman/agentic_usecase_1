# client.py
import asyncio
from fastmcp import Client

async def main():
    """
    An asynchronous function to connect to the MCP server and interact with its tools.
    """
    print("CLIENT: Attempting to connect to the server...")

    # 1. Connect to the server.py script.
    #    FastMCP automatically infers the STDIO transport for .py files.
    async with Client("server.py") as client:
        print("CLIENT: Connection successful!")

        # 2. List the available tools on the server
        tools = await client.list_tools()
        print(f"CLIENT: Found available tools: {[tool.name for tool in tools]}")
        print("-" * 20)

        # 3. Call the 'add' tool
        print("CLIENT: Calling the 'add' tool with a=10, b=5")
        add_result = await client.call_tool("add", {"a": 10, "b": 5})
        # The actual return value is inside the result object
        add_value = add_result.content[0].text
        print(f"CLIENT: Received result from 'add': {add_value}")
        print("-" * 20)

        # 4. Call the 'subtract' tool
        print("CLIENT: Calling the 'subtract' tool with a=100, b=42")
        subtract_result = await client.call_tool("subtract", {"a": 100, "b": 42})
        subtract_value = subtract_result.content[0].text
        print(f"CLIENT: Received result from 'subtract': {subtract_value}")

if __name__ == "__main__":
    asyncio.run(main())