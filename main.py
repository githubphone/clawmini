#!/usr/bin/env python3
"""
ClawMini - 轻量级AI助手整合工具
整合nanoclaw的轻量化设计和aionui的多功能性，借鉴clawx的用户界面
"""
import asyncio
import sys
import os
from src.core import CoreEngine
from adapters.console_adapter import ConsoleAdapter
from adapters.simple_ai_backend import get_available_backends


def setup_engine():
    """设置核心引擎并注册组件"""
    engine = CoreEngine()
    
    # 注册AI后端
    backends = get_available_backends()
    for name, backend_func in backends.items():
        engine.register_ai_backend(name, backend_func)
    
    # 注册控制台适配器
    console_adapter = ConsoleAdapter(engine)
    engine.register_adapter("console", console_adapter)
    
    return engine


def run_gui_app():
    """运行GUI应用程序"""
    from gui.main_window import ClawMiniGUI
    
    engine = setup_engine()
    gui = ClawMiniGUI(engine)
    
    # 更新GUI中的AI后端选项
    backends = get_available_backends()
    gui.update_ai_backends({**backends, "default": backends["qwen"]})
    
    print("启动 ClawMini GUI...")
    gui.run()


async def run_cli_app():
    """运行CLI应用程序（用于测试）"""
    engine = setup_engine()
    
    print("ClawMini CLI 模式")
    print("输入 'quit' 退出，输入 'save' 保存内存")
    
    while True:
        try:
            user_input = input("\n您: ").strip()
            
            if user_input.lower() == 'quit':
                print("再见！")
                break
            elif user_input.lower() == 'save':
                engine.memory_manager.save_memory()
                print("内存已保存")
                continue
            elif user_input.lower() == 'show_tasks':
                print(f"当前任务数: {len(engine.task_scheduler.tasks)}")
                continue
            elif user_input == '':
                continue
            
            # 处理消息
            response = await engine.process_message(
                "console", 
                {
                    "content": user_input,
                    "conversation_id": "cli_session",
                    "sender": "user"
                }
            )
            
            print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


def main():
    """主函数"""
    print("欢迎使用 ClawMini - 轻量级AI助手")
    print("整合了nanoclaw的轻量化设计和aionui的多功能性")
    
    # 检查命令行参数以决定运行模式
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # 运行CLI模式
        asyncio.run(run_cli_app())
    else:
        # 默认运行GUI模式
        run_gui_app()


if __name__ == "__main__":
    main()