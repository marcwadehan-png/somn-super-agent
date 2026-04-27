# Support

## 📚 Documentation

- [README.md](README.md) - 项目概览
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [ROADMAP.md](ROADMAP.md) - 发展路线图
- [CHANGELOG.md](CHANGELOG.md) - 版本变更记录
- [SECURITY.md](SECURITY.md) - 安全策略

## 💬 Community Support

### GitHub Discussions
For general questions, ideas, and community discussions:
- [GitHub Discussions](https://github.com/your-repo/somn/discussions)

### GitHub Issues
For bug reports and feature requests:
- [Bug Reports](https://github.com/your-repo/somn/issues/new?template=bug_report.yml)
- [Feature Requests](https://github.com/your-repo/somn/issues/new?template=feature_request.yml)

## 🆘 Getting Help

### Quick Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| 模块导入失败 | `pip install -e somn` |
| 模型无法连接 | 检查 Ollama 服务: `ollama list` |
| API 服务启动失败 | 检查端口占用: `netstat -ano \| findstr :8964` |
| 测试失败 | `pytest somn/tests/ -v --tb=short` |

### 运行健康检查
```bash
python somn/scripts/health_check.py
```

### 获取详细日志
```bash
# 实时日志
tail -f somn/logs/somn.log

# 搜索错误
grep -i error somn/logs/somn.log
```

## 📧 Contact

- **邮箱**: marcwadehan@gmail.com
- **GitHub**: https://github.com/your-repo/somn

## 💡 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Pull request process
- Testing requirements

## 🐛 Reporting Issues

Before reporting an issue, please:
1. Search existing issues
2. Update to the latest version
3. Run health check script
4. Provide environment details:
   - Python version
   - Operating system
   - Error logs
   - Steps to reproduce

## ⭐ Starring

If Somn is useful to you, star the repository to show your support!

---

*Last updated: 2026-04-27*
