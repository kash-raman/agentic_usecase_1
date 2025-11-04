#!/bin/bash

# A script to run all services for the Document Verification project.
# It starts the Java backend, the two Python MCP servers, and the client orchestrator.
# Press Ctrl+C to stop this script and it will shut down all background services.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Cleanup Function ---
# This function will be called when the script is interrupted (e.g., by Ctrl+C).
cleanup() {
    echo -e "\n\n[SCRIPT] Caught interrupt signal. Shutting down all services..."
    
    # Kill each process using the PIDs we saved.
    # The '2>/dev/null' part suppresses "No such process" errors if a process is already dead.
    kill $JAVA_PID 2>/dev/null
    kill $WATCHER_PID 2>/dev/null
    kill $DOC_SERVER_PID 2>/dev/null
    
    echo "[SCRIPT] All services stopped. Exiting."
    exit 0
}

# --- Trap Setup ---
# 'trap' registers the 'cleanup' function to be executed on SIGINT (Ctrl+C) and SIGTERM.
trap cleanup SIGINT SIGTERM

# --- Main Script Logic ---

echo "[SCRIPT] Starting all services..."

# 1. Start the Spring Boot Java Backend
echo "[SCRIPT] Building and starting the Java verification service..."
(cd verification-service && ./mvnw spring-boot:run &)
JAVA_PID=$! # Save the Process ID (PID) of the last backgrounded command
echo "[SCRIPT] Java service started with PID: $JAVA_PID"

# 2. Start the Python Watcher MCP Server
echo "[SCRIPT] Starting the Python Watcher Server..."
uv run ./src/doc_verify/file_watcher.py &
WATCHER_PID=$!
echo "[SCRIPT] Watcher Server started with PID: $WATCHER_PID"

# 3. Start the Python Document MCP Server
echo "[SCRIPT] Starting the Python Document Server..."
uv run ./src/doc_verify/doc_server.py &
DOC_SERVER_PID=$!
echo "[SCRIPT] Document Server started with PID: $DOC_SERVER_PID"

# 4. Wait for servers to initialize
echo "[SCRIPT] Waiting 10 seconds for all servers to initialize properly..."
sleep 10

# 5. Start the Python Orchestrator Client in the FOREGROUND
echo -e "\n[SCRIPT] Starting the Orchestrator Client. System is now live."
echo "[SCRIPT] Press Ctrl+C to shut everything down."
echo "--------------------------------------------------------"
uv run ./src/doc_verify/orch_client.py

# The script will stay here until the orchestrator is stopped.
# If the orchestrator exits, we should also clean up.
cleanup