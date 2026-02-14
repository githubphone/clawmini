"""
GUI module inspired by clawx desktop interface
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import asyncio
import threading
from src.core import CoreEngine


class ClawMiniGUI:
    """Main GUI window for ClawMini"""
    
    def __init__(self, engine: CoreEngine):
        self.engine = engine
        self.root = tk.Tk()
        self.root.title("ClawMini - 轻量AI助手")
        self.root.geometry("800x600")
        
        # 设置主框架
        self.setup_main_layout()
        
        # 初始化AI后端选择
        self.setup_ai_backends()
        
        # 启动异步事件循环
        self.async_loop = None
        self.start_async_loop()
    
    def setup_main_layout(self):
        """设置主界面布局"""
        # 创建主分割框架
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板 - 控制区域
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # 右侧面板 - 聊天区域
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=3)
        
        # 左侧控制面板
        self.setup_control_panel(left_frame)
        
        # 右侧聊天界面
        self.setup_chat_area(right_frame)
    
    def setup_control_panel(self, parent):
        """设置左侧控制面板"""
        # AI模型选择
        ttk.Label(parent, text="AI模型:").pack(pady=(0, 5))
        self.ai_var = tk.StringVar(value="default")
        self.ai_combo = ttk.Combobox(
            parent, 
            textvariable=self.ai_var,
            values=["default"],
            state="readonly"
        )
        self.ai_combo.pack(fill=tk.X, pady=(0, 10))
        
        # 适配器选择
        ttk.Label(parent, text="消息源:").pack(pady=(0, 5))
        self.adapter_var = tk.StringVar(value="console")
        self.adapter_combo = ttk.Combobox(
            parent,
            textvariable=self.adapter_var,
            values=["console", "whatsapp", "telegram"],
            state="readonly"
        )
        self.adapter_combo.pack(fill=tk.X, pady=(0, 10))
        
        # 任务管理
        ttk.Label(parent, text="任务管理:").pack(pady=(10, 5))
        task_frame = ttk.Frame(parent)
        task_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(task_frame, text="查看任务", command=self.show_tasks).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(task_frame, text="添加任务", command=self.add_task).pack(side=tk.LEFT)
        
        # 内存管理
        ttk.Label(parent, text="内存管理:").pack(pady=(10, 5))
        ttk.Button(parent, text="保存内存", command=self.save_memory).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(parent, text="加载内存", command=self.load_memory).pack(fill=tk.X, pady=(0, 5))
        
        # 日志显示
        ttk.Label(parent, text="日志:").pack(pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(parent, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_chat_area(self, parent):
        """设置右侧聊天区域"""
        # 聊天历史
        self.chat_history = scrolledtext.ScrolledText(
            parent, 
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 输入区域
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X)
        
        self.user_input = tk.Text(input_frame, height=3)
        self.user_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 5))
        
        send_button = ttk.Button(input_frame, text="发送", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
        
        # 绑定回车键发送消息
        self.user_input.bind("<Control-Return>", lambda e: self.send_message())
    
    def setup_ai_backends(self):
        """初始化AI后端选项"""
        # 这里会根据注册的后端动态更新选项
        pass
    
    def update_ai_backends(self, backends):
        """更新AI后端下拉列表"""
        self.ai_combo['values'] = list(backends.keys())
        if backends:
            self.ai_var.set(list(backends.keys())[0])
    
    def add_log(self, message):
        """向日志区域添加消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def add_chat_message(self, sender, message):
        """向聊天区域添加消息"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)
    
    def get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def send_message(self):
        """发送用户输入的消息"""
        message = self.user_input.get("1.0", tk.END).strip()
        if not message:
            return
        
        # 显示用户消息
        self.add_chat_message("你", message)
        self.user_input.delete("1.0", tk.END)
        
        # 异步处理消息
        asyncio.run_coroutine_threadsafe(
            self.process_user_message(message),
            self.async_loop
        )
    
    async def process_user_message(self, message):
        """异步处理用户消息"""
        try:
            # 使用引擎处理消息
            response = await self.engine.process_message(
                self.adapter_var.get(), 
                {
                    "content": message,
                    "conversation_id": "gui_session",
                    "sender": "user"
                }
            )
            
            # 显示AI响应
            self.root.after(0, lambda: self.add_chat_message("AI", str(response)))
            self.root.after(0, lambda: self.add_log(f"处理消息: {message[:50]}..."))
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            self.root.after(0, lambda: self.add_chat_message("系统", error_msg))
            self.root.after(0, lambda: self.add_log(error_msg))
    
    def show_tasks(self):
        """显示当前任务"""
        self.add_log("显示任务功能待实现")
    
    def add_task(self):
        """添加新任务"""
        self.add_log("添加任务功能待实现")
    
    def save_memory(self):
        """保存内存"""
        self.engine.memory_manager.save_memory()
        self.add_log("内存已保存")
    
    def load_memory(self):
        """加载内存"""
        self.engine.memory_manager._load_memory()
        self.add_log("内存已加载")
    
    def start_async_loop(self):
        """启动异步事件循环"""
        def run_loop():
            self.async_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.async_loop)
            self.async_loop.run_forever()
        
        thread = threading.Thread(target=run_loop, daemon=True)
        thread.start()
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()