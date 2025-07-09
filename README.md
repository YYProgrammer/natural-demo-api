# Natural Demo API

一个基于FastAPI的订单管理系统后端API服务，使用uv进行依赖管理，支持ruff代码检查和mypy类型检查。

## 系统要求

- Python 3.11 或更高版本
- uv 包管理器（推荐）或 pip
- 操作系统：Windows, macOS, Linux

## 环境安装

### 1. 安装 uv 包管理器（推荐）

#### macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 或者使用 pip 安装:
```bash
pip install uv
```

### 2. 克隆项目
```bash
git clone <repository-url>
cd natural-demo-api
```

### 3. 安装项目依赖

#### 使用 uv（推荐）:
```bash
# 安装生产环境依赖
uv sync

# 安装包含开发工具的依赖
uv sync --group dev
```

#### 使用传统方式:
```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -e .
pip install -e ".[dev]"
```

#### 使用 Makefile:
```bash
# 生成新的虚拟环境并安装依赖
make gen

# 仅安装依赖
make install
```

## 服务器运行

### 开发环境运行

#### 方式1: 使用 uv run（推荐）
```bash
uv run python main.py
```

#### 方式2: 使用 uvicorn 直接运行
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 5001
```

#### 方式3: 使用 Makefile
```bash
make dev
```

#### 方式4: 使用虚拟环境
```bash
# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 运行应用
python main.py
```

### 生产环境运行

#### 使用 uvicorn:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 5001
```

#### 使用 gunicorn（需要安装）:
```bash
uv add gunicorn
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5001
```

## 访问服务

启动服务器后，可以通过以下方式访问：

- **API 文档**: http://localhost:5001/docs
- **健康检查**: http://localhost:5001/planning-api/api/health
- **API 基础路径**: http://localhost:5001/planning-api/api

## 代码质量工具

### 代码检查
```bash
# 运行 ruff 代码检查
make lint

# 运行 mypy 类型检查
make type-check

# 运行所有检查
make check
```

### 代码格式化
```bash
# 格式化代码
make fix
```

### 运行所有质量检查
```bash
make all
```

## API 端点

- `GET /planning-api/api/` - 返回欢迎信息
- `GET /planning-api/api/health` - 健康检查端点
- `GET /docs` - 交互式API文档（Swagger UI）

## 开发指南

### 添加新依赖
```bash
# 使用 uv
uv add package-name

# 添加开发依赖
uv add --dev package-name
```

### 项目结构
```
natural-demo-api/
├── main.py              # 应用入口
├── pyproject.toml       # 项目配置
├── Makefile            # 构建脚本
├── src/
│   ├── api/            # API 模块
│   │   ├── api_config.py
│   │   ├── hello/      # Hello 模块
│   │   └── planning/   # Planning 模块
│   └── base/           # 基础模块
│       └── settings/   # 配置设置
```

## 配置说明

- **端口**: 默认运行在 5001 端口
- **API 前缀**: `/planning-api/api`
- **开发模式**: 支持热重载
- **文档**: 自动生成 Swagger UI 文档

## 故障排除

### 常见问题

1. **端口被占用**:
   ```bash
   # 查看端口占用
   lsof -i :5001
   # 或修改端口
   make dev port=8080
   ```

2. **依赖安装失败**:
   ```bash
   # 清理缓存重新安装
   uv cache clean
   uv sync
   ```

3. **虚拟环境问题**:
   ```bash
   # 重新生成虚拟环境
   make gen
   ```

## 可用的 Make 命令

运行 `make help` 查看所有可用命令：

- `make dev` - 启动开发服务器
- `make lint` - 运行代码检查
- `make type-check` - 运行类型检查
- `make fix` - 格式化代码
- `make check` - 运行所有检查
- `make gen` - 生成新的虚拟环境
- `make install` - 安装依赖