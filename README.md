# Somn (索姆)

**Somn** — 基于大语言模型的自主进化智能体，集成多层级推理引擎与知识系统。

**Somn** — An autonomous LLM-powered agent with multi-tier reasoning engines and knowledge systems.

![Version](https://img.shields.io/badge/version-v6.2.0-blue)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)

---

## 核心特性 | Key Features

- **双脑架构 Dual Brain** — Gemma4 (主脑) + Llama-3.2 (副脑)，本地/云端双模式
- **142 推理引擎** — LongCoT / ToT / GoT / ReAct 四大推理体系
- **21 智慧学派** — 儒/道/佛/法/兵家/心理学/经济学等
- **21 格知识系统** — 动态网状知识库，跨领域关联
- **神经记忆 v21** — Hebbian 学习 + 三层记忆架构
- **PyQt6 前端** — 前后端分离，WebSocket 实时通信
- **FastAPI 后端** — RESTful API，61 个端点

---

## 快速开始 | Quick Start

```bash
# 克隆 / Clone
git clone https://github.com/marcwadehan-png/somn-agent.git
cd somn-agent

# 安装依赖 / Install
pip install -r requirements.txt
pip install -r Somn-GUI/requirements.txt

# 启动后端 / Start Backend
python -m uvicorn api.main:app --reload

# 启动前端 / Start Frontend (新终端)
python Somn-GUI/main.py
```

---

## 项目结构 | Project Structure

```
somn/                          # Python 子包
├── api/                       # FastAPI 服务 (61 端点)
├── global_control_center/    # 全局控制中心
├── knowledge_cells/          # 21 格知识系统
├── smart_office_assistant/   # 核心引擎
Somn-GUI/                      # PyQt6 前端
api/                           # FastAPI 服务入口
docs/                          # 文档 (ADR 架构决策)
```

---
## 联系
邮箱：marcwadehan@gmail.com

## 协议 | License

AGPL v3 — 详见 [LICENSE](LICENSE)

---

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request。详见 [CONTRIBUTING.md](CONTRIBUTING.md)
