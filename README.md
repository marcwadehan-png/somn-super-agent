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
smart_office_assistant/       # 核心引擎 (主程序)
api/                          # FastAPI 服务 (61 端点)
Somn-GUI/                     # PyQt6 前端
knowledge_cells/              # 21 格知识系统
docs/                         # 文档 (ADR 架构决策)
tests/                        # 测试套件
```

---

## 联系
邮箱：marcwadehan@gmail.com

## 协议 | License

AGPL v3 — 详见 [LICENSE](LICENSE)

---

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request。详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🛠️ 招募贡献者 | Call for Contributors

**Somn** 是开源协作项目，我们欢迎各类开发者加入！

### 🔍 我们需要的帮助

| 领域 | 描述 | 难度 |
|------|------|------|
| **推理引擎优化** | 提升 LongCoT/ToT/GoT/ReAct 推理效率 | ⭐⭐⭐ |
| **知识系统扩展** | 丰富 21 智慧学派与知识格子内容 | ⭐⭐ |
| **前端开发** | PyQt6 UI 优化与新功能开发 | ⭐⭐ |
| **后端架构** | FastAPI 服务扩展与性能优化 | ⭐⭐⭐ |
| **测试覆盖** | 编写单元测试与集成测试 | ⭐ |
| **文档翻译** | 中英文文档互译 | ⭐ |

### 🚀 如何开始

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-idea`
3. 提交代码：`git commit -m 'Add: your feature'`
4. 推送分支：`git push origin feature/your-idea`
5. 提交 **Pull Request**

### 💬 社区交流

- 📧 邮箱：marcwadehan@gmail.com
- 🐛 问题反馈：[GitHub Issues](https://github.com/marcwadehan-png/somn-agent/issues)
- 💡 功能建议：[GitHub Discussions](https://github.com/marcwadehan-png/somn-agent/discussions)

### 🌟 贡献者福利

- 贡献代码将出现在项目的 **Contributors** 列表
- 优秀贡献者可获得 **Repository Write** 权限
- 定期评选 **月度最佳贡献者**

**无论大小，每一份贡献都值得感谢！**
