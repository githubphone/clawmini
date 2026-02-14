# ClawMini

一个轻量级的AI助手工具，结合了nanoclaw的轻量化设计、aionui的多功能AI集成以及clawx的用户友好界面。

## 特性

- **轻量级**: 继承nanoclaw的设计理念，可在低成本设备上运行
- **多AI支持**: 整合多种AI模型，如Qwen、Claude、Gemini等
- **安全沙箱**: 采用容器化设计确保安全
- **图形界面**: 提供类似clawx的桌面体验
- **消息集成**: 支持WhatsApp等多种消息平台
- **本地运行**: 数据完全在本地处理，保护隐私

## 架构概览

```
┌─────────────────┐
│   GUI Layer     │ ← clawx-inspired desktop interface
├─────────────────┤
│   AI Router     │ ← aionui-style AI model selection
├─────────────────┤
│  Core Engine    │ ← nanoclaw-inspired lightweight core
├─────────────────┤
│   Adapters      │ ← Message platforms, storage, etc.
└─────────────────┘
```

## 技术栈

- Python 3.x (保持轻量化)
- Tkinter/PyQt (GUI)
- AsyncIO (并发处理)
- SQLite (轻量存储)
- Docker (安全沙箱)

## 目标

打造一个比OpenClaw更轻便，但功能丰富的AI助手工具，特别适合在资源受限的环境中运行。