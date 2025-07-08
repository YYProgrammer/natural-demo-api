from flask import Flask, jsonify, request, Response
import json
import time
import os

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

@app.route('/v1.0/invoke/planning-api/method/ai_phone/planning/completions', methods=['POST'])
def planning_completions():
    """
    规划完成API端点 - 流式响应
    接收参数: session_id, stream, query
    返回: 流式JSON数据
    """
    # 获取请求参数
    data = request.get_json()
    session_id = data.get('session_id')
    stream = data.get('stream', True)
    query = data.get('query', '')
    
    def generate_stream():
        # 读取 response/a_to_b/1.json 文件
        try:
            with open('response/a_to_b/1.json', 'r', encoding='utf-8') as f:
                response = json.load(f)
            
            # 更新 session_id 和 focus 字段
            if session_id:
                response['session_id'] = session_id
            if query and 'screens' in response and len(response['screens']) > 0:
                response['screens'][0]['focus'] = query
                
        except FileNotFoundError:
            # 如果文件不存在，使用默认响应
            response = {
                "session_id": session_id,
                "screens": [{
                    "name": "main",
                    "key": "e77b28b0c42672dba773d7564f6dda4a",
                    "state": "active",
                    "title": "Group Travel Planning",
                    "description": "Main screen for collaborative travel planning and coordination.",
                    "icon": "",
                    "focus": query,
                    "interaction_value": "",
                    "interaction_template": "",
                    "cards": []
                }]
            }
        except json.JSONDecodeError:
            # 如果 JSON 解析失败，使用默认响应
            response = {
                "session_id": session_id,
                "error": "JSON decode error in response file"
            }
        
        yield f"data: {json.dumps(response)}\n\n"
        time.sleep(0.1)
        
        # 重复发送相同的响应（模拟最后几次相同的数据）
        for _ in range(2):
            yield f"data: {json.dumps(response)}\n\n"
            time.sleep(0.1)
    
    return Response(generate_stream(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 