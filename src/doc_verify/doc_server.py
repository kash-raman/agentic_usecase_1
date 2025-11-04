import json
import aiohttp
from fastmcp import FastMCP

mcp = FastMCP("RealDocumentVerificationServer")
SPRING_BOOT_BASE_URL = "http://localhost:8080"

@mcp.tool
async def verify_bank_statement(file_path: str) -> str:
    """
    Reads a local file (PDF or JSON) and sends it to the Spring Boot backend
    for verification, returning the extracted data.
    """
    print(f"DOC_SERVER: Sending file '{file_path}' to Java backend...")
    try:
        async with aiohttp.ClientSession() as session:
            # aiohttp requires reading the file into a FormData object
            data = aiohttp.FormData()
            data.add_field('file',
                           open(file_path, 'rb'),
                           filename=file_path.split('/')[-1],
                           content_type='application/octet-stream') # Let the server decide content type

            async with session.post(f"{SPRING_BOOT_BASE_URL}/verify/bank-statement", data=data) as response:
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                result = await response.json()
                print(f"DOC_SERVER: Received bank data from backend: {result}")
                return json.dumps(result)
    except Exception as e:
        print(f"DOC_SERVER_ERROR: Could not verify bank statement: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool
async def fetch_bank_statement(firstName: str, lastName: str, address: str) -> str:
    """
    Calls the Spring Boot backend with PII to get a mocked bank statement.
    """
    print(f"DOC_SERVER: verifying bank statements using Java backend...")
    try:
        params = {"firstName": firstName, "lastName": lastName, "address": address}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SPRING_BOOT_BASE_URL}/bank-statement", params=params) as response:
                response.raise_for_status()
                result = await response.json()
                print(f"DOC_SERVER: Received credit data from backend: {result}")
                return json.dumps(result)
    except Exception as e:
        print(f"DOC_SERVER_ERROR: Could not verify bank statement: {e}")
        return json.dumps({"error": str(e)})
    
@mcp.tool
async def verify_credit_report(firstName: str, lastName: str, ssn: str) -> str:
    """
    Calls the Spring Boot backend with PII to get a mocked credit report.
    """
    print(f"DOC_SERVER: Getting credit report for {firstName} {lastName} from Java backend...")
    try:
        params = {"firstName": firstName, "lastName": lastName, "ssn": ssn}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SPRING_BOOT_BASE_URL}/credit-report", params=params) as response:
                response.raise_for_status()
                result = await response.json()
                print(f"DOC_SERVER: Received credit data from backend: {result}")
                return json.dumps(result)
    except Exception as e:
        print(f"DOC_SERVER_ERROR: Could not get credit report: {e}")
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    print("Document Verification Server (API Bridge) is running...")
    mcp.run(transport="http", port=8002)