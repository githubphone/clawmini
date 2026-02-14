"""
Core engine inspired by nanoclaw's lightweight design
"""
import asyncio
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class MemoryManager:
    """Lightweight memory management inspired by nanoclaw"""
    
    def __init__(self, storage_path: str = "./memory.json"):
        self.storage_path = storage_path
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from persistent storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"conversations": {}, "tasks": [], "preferences": {}}
    
    def save_memory(self):
        """Save memory to persistent storage"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def add_conversation(self, conv_id: str, message: Dict[str, Any]):
        """Add a message to a conversation"""
        if conv_id not in self.memory["conversations"]:
            self.memory["conversations"][conv_id] = []
        self.memory["conversations"][conv_id].append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
        self.save_memory()


class TaskScheduler:
    """Lightweight task scheduler inspired by nanoclaw"""
    
    def __init__(self):
        self.tasks = {}
    
    async def add_task(self, task_id: str, coroutine, delay: int):
        """Schedule a task to run after delay seconds"""
        self.tasks[task_id] = asyncio.create_task(self._run_delayed(coroutine, delay))
    
    async def _run_delayed(self, coroutine, delay: int):
        """Internal method to run a coroutine after delay"""
        await asyncio.sleep(delay)
        await coroutine
    
    def cancel_task(self, task_id: str):
        """Cancel a scheduled task"""
        if task_id in self.tasks:
            self.tasks[task_id].cancel()
            del self.tasks[task_id]


class AIBackendRouter:
    """AI backend router inspired by aionui's multi-AI support"""
    
    def __init__(self):
        self.backends = {}
        self.default_backend = None
    
    def register_backend(self, name: str, backend_callable):
        """Register an AI backend"""
        self.backends[name] = backend_callable
        if self.default_backend is None:
            self.default_backend = name
    
    async def route_request(self, prompt: str, backend_name: Optional[str] = None):
        """Route request to appropriate AI backend"""
        if backend_name is None:
            backend_name = self.default_backend
        
        if backend_name not in self.backends:
            raise ValueError(f"Unknown backend: {backend_name}")
        
        return await self.backends[backend_name](prompt)


class CoreEngine:
    """Main core engine combining nanoclaw lightweight design with aionui features"""
    
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.task_scheduler = TaskScheduler()
        self.ai_router = AIBackendRouter()
        self.adapters = {}
    
    def register_adapter(self, name: str, adapter):
        """Register a communication adapter (WhatsApp, etc.)"""
        self.adapters[name] = adapter
    
    def register_ai_backend(self, name: str, backend_callable):
        """Register an AI backend"""
        self.ai_router.register_backend(name, backend_callable)
    
    async def process_message(self, adapter_name: str, message_data: Dict[str, Any]):
        """Process an incoming message through the engine"""
        # Add to memory
        conv_id = message_data.get("conversation_id", "default")
        self.memory_manager.add_conversation(conv_id, message_data)
        
        # Route to AI backend
        prompt = message_data.get("content", "")
        ai_response = await self.ai_router.route_request(prompt)
        
        # Send response back through adapter
        if adapter_name in self.adapters:
            await self.adapters[adapter_name].send_response(ai_response)
        
        return ai_response