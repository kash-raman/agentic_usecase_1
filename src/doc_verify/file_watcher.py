# watcher_server.py
import asyncio
import json
import os
import threading
from fastmcp import FastMCP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIRECTORY = "verification_jobs"
job_queue = asyncio.Queue() # A queue to hold pending jobs

class JobHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop
        self.processed_jobs = set()

    def on_created(self, event):
        if event.is_directory:
            return

        job_id = self.get_job_id(event.src_path)
        if not job_id or job_id in self.processed_jobs:
            return

        credit_path = os.path.join(WATCH_DIRECTORY, f"{job_id}_credit.json")
        bank_path = os.path.join(WATCH_DIRECTORY, f"{job_id}_bank.json")

        if os.path.exists(credit_path) and os.path.exists(bank_path):
            print(f"WATCHER: Detected complete job '{job_id}'. Adding to queue.")
            self.processed_jobs.add(job_id)
            
            # This is the crucial part: define the job and the tasks it requires.
            job_data = {
                "job_id": job_id,
                "tasks": [
                    { "tool_name": "verify_credit_report", "file_path": credit_path },
                    { "tool_name": "verify_bank_statement", "file_path": bank_path }
                ]
            }
            # Safely put the job into the asyncio queue from the watchdog thread
            self.loop.call_soon_threadsafe(job_queue.put_nowait, job_data)

    def get_job_id(self, file_path):
        filename = os.path.basename(file_path)
        if "_credit.json" in filename: return filename.replace("_credit.json", "")
        if "_bank.json" in filename: return filename.replace("_bank.json", "")
        return None

# --- MCP Server Setup ---
mcp = FastMCP("FileWatcherServer")

@mcp.tool
async def get_new_job() -> str:
    """
    Waits for a new verification job to be ready and returns its details.
    This is a long-polling tool; it will not return until a job is available.
    """
    print("WATCHER: A client is waiting for a new job...")
    job = await job_queue.get()
    print(f"WATCHER: Delivering job '{job['job_id']}' to the client.")
    return json.dumps(job)

def start_file_watcher(loop):
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)
    
    event_handler = JobHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()
    print(f"File watcher started in background, monitoring '{WATCH_DIRECTORY}'")
    observer.join() # This will block the thread until it's stopped

if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    
    # Run the file watcher in a separate thread
    watcher_thread = threading.Thread(target=start_file_watcher, args=(main_loop,), daemon=True)
    watcher_thread.start()
    
    print("File Watcher MCP Server is running...")
    mcp.run(transport="http", port=8001)