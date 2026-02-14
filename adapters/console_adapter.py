"""
Console adapter for testing purposes
"""
import asyncio
from typing import Dict, Any


class ConsoleAdapter:
    """控制台适配器，用于测试和演示"""
    
    def __init__(self, engine):
        self.engine = engine
        self.name = "console"
    
    async def start(self):
        """启动适配器"""
        print("控制台适配器已启动")
        await self.listen_for_messages()
    
    async def listen_for_messages(self):
        """监听消息（在实际实现中可能是长期运行的）"""
        print("控制台适配器正在监听消息...")
        while True:
            try:
                # 在真实场景中，这里会接收实际消息
                # 现在我们只是模拟一个简单的输入循环
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                break
    
    async def send_response(self, response):
        """发送响应到控制台"""
        print(f"控制台适配器发送响应: {response}")
    
    def format_message(self, message_data: Dict[str, Any]) -> str:
        """格式化消息数据"""
        return f"[Console] {message_data.get('content', '')}"