# Python API 测试项目

这是一个基础的 Python Flask API 项目，提供简单的测试接口。

## 项目结构

```
natural-api-test/
├── app.py           # 主应用文件
├── requirements.txt # 依赖文件
└── README.md       # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python app.py
```

项目将在 `http://localhost:5001` 上运行。

## API 接口

### 1. 测试接口

- **URL**: `/api/test`
- **方法**: GET
- **返回**: `{"test": "v1"}`

### 2. 健康检查

- **URL**: `/`
- **方法**: GET
- **返回**: `{"status": "ok", "message": "API服务正在运行"}`

## 使用示例

### 使用 curl 调用 API

```bash
# 测试API接口
curl http://localhost:5001/api/test

# 健康检查
curl http://localhost:5001/
```

### 预期返回结果

测试接口返回：

```json
{
  "test": "v1"
}
```

健康检查返回：

```json
{
  "status": "ok",
  "message": "API服务正在运行"
}
```

## 开发模式

项目已配置为开发模式，修改代码后会自动重启服务。
