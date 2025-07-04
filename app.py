from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test', methods=['GET'])
def test_api():
    """
    测试API端点
    返回: {"test": "v1"}
    """
    return jsonify({"test": "v1"})

@app.route('/', methods=['GET'])
def health_check():
    """
    健康检查端点
    """
    return jsonify({"status": "ok", "message": "API服务正在运行"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 