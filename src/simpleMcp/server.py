# server.py
from fastmcp import FastMCP

# 1. Initialize the FastMCP server with a name
mcp = FastMCP("CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """
    Adds two integer numbers together and returns the sum.
    The docstring is used as the description for the tool.
    """
    print(f"SERVER: Received add request with a={a}, b={b}")
    result = a + b
    print(f"SERVER: Returning result: {result}")
    return result

@mcp.tool
def subtract(a: int, b: int) -> int:
    """
    Subtracts the second integer from the first and returns the difference.
    """
    print(f"SERVER: Received subtract request with a={a}, b={b}")
    result = a - b
    print(f"SERVER: Returning result: {result}")
    return result

# 2. This block allows the server to be run directly
#    You can also run it from the command line with `fastmcp run server.py`
if __name__ == "__main__":
    mcp.run()