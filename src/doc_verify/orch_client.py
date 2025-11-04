# orchestrator_client.py
import asyncio
import json
from fastmcp import Client
WATCHER_SERVER_URL = "http://127.0.0.1:8001"
DOCUMENT_SERVER_URL = "http://127.0.0.1:8002"
async def main( ):
    print("Orchestrator Client started. Waiting for jobs from the Watcher Server...")
    while True:
        try:
            job_data = {
                "job_id": "job-001",
                "tasks": [
                    {
                        "tool_name": "verify_credit_report",
                        "arguments": {
                            "firstName": "John",
                            "lastName": "Doe",
                            "ssn": "999-99-9999"
                        }
                    },
                    {
                        "tool_name": "verify_bank_statement",
                        "arguments": {  "firstName": "John",
                            "lastName": "Doe",
                            "address": "123 Main St, Anytown, USA"}
                    }
                ]
            }
            # Safely put the job into the asyncio queue
            #self.loop.call_soon_threadsafe(job_queue.put_nowait, job_data)
            # 1. Connect to the watcher server and wait for a job
            async with Client(WATCHER_SERVER_URL) as watcher_client:
                job_result = await watcher_client.call_tool("get_new_job")
                job_data = json.loads(job_result.content[0].text)
            
            job_id = job_data['tasks_to_run'] = job_data['tasks']
            print(f"\nORCHESTRATOR: Received job '{job_id}'. Processing {len(tasks_to_run)} tasks.")

            # 2. Connect to the document server to execute the tasks
            async with Client(DOCUMENT_SERVER_URL) as doc_client:
                # Dynamically create an asyncio task for each task in the job description
                mcp_tasks = []
                for task in tasks_to_run:
                    tool_name = task['tool_name']
                    file_path = task['file_path']
                    print(f"ORCHESTRATOR: Queuing tool '{tool_name}' for file '{file_path}'")
                    mcp_tasks.append(doc_client.call_tool(tool_name, {"file_path": file_path}))
                
                # 3. Run all verification tasks concurrently
                results = await asyncio.gather(*mcp_tasks)
            
            # 4. Process the results (the matching logic)
            processed_results = {}
            for i, task in enumerate(tasks_to_run):
                # Use the tool_name to key the results dictionary
                tool_name = task['tool_name']
                data = json.loads(results[i].content[0].text)
                processed_results[tool_name] = data

            # The comparison logic is now more generic
            credit_data = processed_results.get('verify_credit_report', {})
            bank_data = processed_results.get('verify_bank_statement', {})

            print(f"ORCHESTRATOR: Credit Report Data: {credit_data}")
            print(f"ORCHESTRATOR: Bank Statement Data: {bank_data}")

            name_match = credit_data.get('name', 'a').lower() == bank_data.get('name', 'b').lower()
            address_match = credit_data.get('address', 'c').lower().replace(',', '') == bank_data.get('address', 'd').lower().replace(',', '')

            print("-" * 30)
            print(f"Verification Result for Job '{job_id}':")
            print(f"  Name Match: {'PASS' if name_match else 'FAIL'}")
            print(f"  Address Match: {'PASS' if address_match else 'FAIL'}")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nORCHESTRATOR: Shutting down.")
            break
        except Exception as e:
            print(f"ORCHESTRATOR: An error occurred: {e}. Waiting for next job.")
            await asyncio.sleep(5) # Wait a bit before retrying

if __name__ == "__main__":
    asyncio.run(main())