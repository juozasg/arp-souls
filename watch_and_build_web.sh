#!/bin/bash

# Directory to watch (current directory by default)
WATCH_DIR="source"


# PID of the background process
PID=""

# Function to kill existing process
kill_process() {
    if [ ! -z "$PID" ]; then
        echo "Stopping existing process (PID: $PID)..."
        kill -TERM $PID 2>/dev/null
        wait $PID 2>/dev/null
    fi
}

# Function to start the process
start_process() {

		./build_web.sh
		python -m http.server -d build/web/ &
    PID=$!
    echo "Started with PID: $PID"
}

# Cleanup on script exit
trap 'kill_process; exit 0' SIGINT SIGTERM

echo "Watching directory: $WATCH_DIR"
echo "Press Ctrl+C to stop"

# Start initial process
start_process

# Watch for file changes using inotifywait
echo "itonifywait $WATCH_DIR..."
inotifywait -m -r -e modify,create,delete,move "$WATCH_DIR" --format '%w%f %e' | while read file event; do
    echo "File changed: $file ($event)"
    kill_process
    sleep 1  # Brief delay to avoid rapid restarts
    start_process
done