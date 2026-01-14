#!/bin/bash

PID_FILE="server.pid"
VENV_ACTIVATE="venv/bin/activate"

start() {
    if [ -f "$PID_FILE" ]; then
        echo "Server appears to be running (PID $(cat $PID_FILE)). Stop it first."
    else
        source $VENV_ACTIVATE
        nohup python manage.py runserver > server.log 2>&1 &
        echo $! > $PID_FILE
        echo "Server started with PID $(cat $PID_FILE). Logs are in server.log"
    fi
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            kill $PID
            echo "Server stopped (PID $PID)."
        else
            echo "PID file exists but process $PID is not running."
        fi
        rm $PID_FILE
    else
        # Fallback: find process by port 8000
        PID=$(lsof -t -i:8000)
        if [ -n "$PID" ]; then
            kill $PID
            echo "Server stopped (PID $PID found via port 8000)."
        else
            echo "No server is running."
        fi
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
