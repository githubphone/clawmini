#!/bin/bash

# ClawMini 启动脚本

cd /workspaces/clawmini

case "$1" in
    gui)
        echo "启动 ClawMini GUI 模式..."
        python3 main.py
        ;;
    cli)
        echo "启动 ClawMini CLI 模式..."
        python3 main.py --cli
        ;;
    install)
        echo "安装依赖..."
        pip install -r requirements.txt
        echo "依赖安装完成"
        ;;
    test)
        echo "运行测试..."
        python3 -m pytest tests/ -v
        ;;
    *)
        echo "用法: $0 {gui|cli|install|test}"
        echo "  gui    - 启动图形界面模式（默认）"
        echo "  cli    - 启动命令行界面模式"
        echo "  install - 安装依赖"
        echo "  test   - 运行测试"
        echo ""
        echo "直接运行 '$0' 将启动GUI模式"
        ;;
esac