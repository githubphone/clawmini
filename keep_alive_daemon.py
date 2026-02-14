#!/usr/bin/env python3
import time
import datetime
import os
import subprocess
import signal
import sys

def signal_handler(sig, frame):
    print('收到终止信号，正在退出...')
    sys.exit(0)

def main():
    # 注册信号处理器以便优雅退出
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("启动 Codespace 保活守护进程...")
    print("按 Ctrl+C 停止")
    
    # 确保日志目录存在
    os.makedirs('/workspaces/clawmini/logs', exist_ok=True)
    
    while True:
        try:
            # 记录心跳
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('/workspaces/clawmini/logs/heartbeat.log', 'a') as f:
                f.write(f"{timestamp}: Heartbeat - Preventing Codespace sleep\n")
            
            # 更新保活文件的时间戳
            with open('/workspaces/clawmini/.keepalive', 'a'):
                os.utime('/workspaces/clawmini/.keepalive', None)
            
            # 执行轻量级git操作以保持连接活跃
            try:
                subprocess.run(['git', 'status'], cwd='/workspaces/clawmini', 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                             timeout=5)
            except subprocess.TimeoutExpired:
                pass
            
            print(f"{timestamp}: 已发送心跳")
            
            # 等待20分钟（1200秒）
            time.sleep(1200)
            
        except Exception as e:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('/workspaces/clawmini/logs/error.log', 'a') as f:
                f.write(f"{timestamp}: Error in keep_alive_daemon - {str(e)}\n")
            time.sleep(60)  # 出错时等待1分钟后重试

if __name__ == "__main__":
    main()