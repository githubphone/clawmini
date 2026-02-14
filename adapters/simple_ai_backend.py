"""
Simple AI backend for demonstration
"""
import asyncio
import random
from typing import Dict, Any


async def simple_qwen_backend(prompt: str) -> str:
    """
    模拟Qwen AI后端
    """
    await asyncio.sleep(0.5)  # 模拟API调用延迟
    
    responses = [
        f"Qwen回应: 我收到了您的消息: '{prompt[:50]}...' 有什么我可以帮助您的吗？",
        f"Qwen分析: 关于'{prompt[:30]}...'，我认为这是一个很好的问题。",
        f"Qwen思考: 让我考虑一下'{prompt[:20]}...'这个问题。",
        f"Qwen回答: 您询问了'{prompt[:40]}...'，我会尽力提供有用的信息。"
    ]
    
    return random.choice(responses)


async def simple_claude_backend(prompt: str) -> str:
    """
    模拟Claude AI后端
    """
    await asyncio.sleep(0.7)  # 模拟API调用延迟
    
    responses = [
        f"Claude回应: 感谢您分享关于'{prompt[:50]}...'的想法，这是一个值得探讨的话题。",
        f"Claude分析: 从我的角度来看，'{prompt[:30]}...'涉及多个层面。",
        f"Claude思考: 我理解您对'{prompt[:20]}...'的关注，让我详细解释。",
        f"Claude回答: 针对您关于'{prompt[:40]}...'的询问，我的看法如下。"
    ]
    
    return random.choice(responses)


async def simple_gemini_backend(prompt: str) -> str:
    """
    模拟Gemini AI后端
    """
    await asyncio.sleep(0.6)  # 模拟API调用延迟
    
    responses = [
        f"Gemini回应: 收到您关于'{prompt[:50]}...'的查询，正在处理中。",
        f"Gemini分析: '{prompt[:30]}...'是一个有趣的问题，让我为您提供信息。",
        f"Gemini思考: 对于'{prompt[:20]}...'，我有以下见解。",
        f"Gemini回答: 关于'{prompt[:40]}...'，这是我的专业建议。"
    ]
    
    return random.choice(responses)


def get_available_backends():
    """
    返回可用的AI后端列表
    """
    return {
        "qwen": simple_qwen_backend,
        "claude": simple_claude_backend,
        "gemini": simple_gemini_backend
    }