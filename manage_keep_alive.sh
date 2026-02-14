#!/bin/bash

DAEMON_NAME="keep_alive_daemon.py"
LOG_DIR="/workspaces/clawmini/logs"

case "$1" in
    start)
        if pgrep -f "$DAEMON_NAME" > /dev/null; then
            echo "守护进程已在运行"
        else
            echo "启动守护进程..."
            nohup python3 /workspaces/clawmini/keep_alive_daemon.py > $LOG_DIR/daemon.log 2>&1 &
            echo "守护进程已启动"
        fi
        ;;
    stop)
        if pgrep -f "$DAEMON_NAME" > /dev/null; then
            echo "停止守护进程..."
            pkill -f "$DAEMON_NAME"
            echo "守护进程已停止"
        else
            echo "守护进程未在运行"
        fi
        ;;
    status)
        if pgrep -f "$DAEMON_NAME" > /dev/null; then
            echo "守护进程正在运行"
            ps aux | grep "$DAEMON_NAME" | grep -v grep
        else
            echo "守护进程未在运行"
        fi
        ;;
    logs)
        if [ -f "$LOG_DIR/heartbeat.log" ]; then
            echo "最近的心跳日志："
            tail -10 "$LOG_DIR/heartbeat.log"
        else
            echo "心跳日志文件不存在"
        fi
        ;;
    *)
        echo "用法: $0 {start|stop|status|logs}"
        exit 1
        ;;
esac