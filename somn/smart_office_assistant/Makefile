# Neural Memory Tests + Code Quality - Makefile shortcut
# Usage: make test / make lint / make quality / make clean
# 依赖: pip install -r requirements-dev.txt

.PHONY: test cov cov-quick lint lint-pylint lint-flake8 lint-complexity quality clean install-deps

# Working directory
PROJECT_ROOT := smart_office_assistant
SRC_DIR := $(PROJECT_ROOT)/src

# ============================================================
# 开发环境安装
# ============================================================
install-deps:
	@echo "安装代码质量检查工具..."
	pip install -r requirements-dev.txt

# ============================================================
# 测试
# ============================================================
test:
	cd $(PROJECT_ROOT) && python -m pytest tests/neural_memory/ -v --tb=short

cov:
	cd $(PROJECT_ROOT) && python -m pytest tests/neural_memory/ -v --tb=short --cov=src/neural_memory --cov-report=term-missing --cov-report=html:htmlcov/neural_memory

cov-quick:
	cd $(PROJECT_ROOT) && python -m pytest tests/neural_memory/ --tb=line -q --cov=src/neural_memory --cov-report=term-missing

# ============================================================
# Linting (pylint)
# ============================================================
lint-pylint:
	@echo "Running Pylint (max-complexity=15)..."
	pylint $(SRC_DIR) \
		--max-complexity=15 \
		--jobs=4 \
		--persistent=yes \
		--output-format=text \
		--disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

# ============================================================
# Linting (flake8)
# ============================================================
lint-flake8:
	@echo "Running Flake8..."
	flake8 $(SRC_DIR) \
		--max-line-length=120 \
		--exclude=data,tests,__pycache__,node_modules \
		--count --statistics --show-source

# ============================================================
# 复杂度分析 (radon)
# ============================================================
lint-complexity:
	@echo "Running Complexity Analysis..."
	@echo "=== McCabe圈复杂度 (>15标记) ==="
	radon cc -a -n 15 $(SRC_DIR)
	@echo ""
	@echo "=== Maintainability Index ==="
	radon mi -s $(SRC_DIR)
	@echo ""
	@echo "=== Raw Metrics ==="
	radon raw -s $(SRC_DIR)

# ============================================================
# 安全检查 (bandit)
# ============================================================
lint-security:
	@echo "Running Security Check..."
	bandit -r $(SRC_DIR) -f screen

# ============================================================
# 完整lint (推荐)
# ============================================================
lint: lint-pylint lint-flake8 lint-complexity lint-security
	@echo ""
	@echo "=== Lint Complete ==="

# ============================================================
# 代码质量完整检查 (包含格式检查)
# ============================================================
quality: lint
	@echo ""
	@echo "=== Code Format Check (black) ==="
	@black --check --diff $(SRC_DIR) || true
	@echo ""
	@echo "=== Import Sort Check (isort) ==="
	@isort --check-only --diff $(SRC_DIR) || true

# ============================================================
# 清理
# ============================================================
clean:
	cd $(PROJECT_ROOT) && rm -rf htmlcov/ .pytest_cache/ test-results.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
