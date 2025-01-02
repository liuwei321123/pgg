from flask import Flask, render_template, request, jsonify
import base64, zlib, lzma, bz2, gzip
import json
import os
from datetime import datetime

app = Flask(__name__)

# 存储环境变量的字典
env_vars = {}

# 存储日志的列表
logs = []

@app.route('/')
def index():
    return render_template('index.html', env_vars=env_vars, logs=logs)

@app.route('/add_env', methods=['POST'])
def add_env():
    name = request.form.get('name')
    value = request.form.get('value')
    
    if name and value:
        env_vars[name] = value
        add_log(f"添加环境变量: {name}")
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "名称和值不能为空"})

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # 这里执行你的主要脚本逻辑
        exec_script()
        add_log("脚本执行成功")
        return jsonify({"status": "success"})
    except Exception as e:
        add_log(f"脚本执行失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

def add_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.insert(0, f"[{timestamp}] {message}")
    if len(logs) > 100:  # 只保留最近100条日志
        logs.pop()

def exec_script():
    # 将环境变量注入到执行环境
    os.environ.update(env_vars)
    
    # 这里放入你的主脚本代码
    script = """
    # 你的代码会在这里执行
    ck = os.environ.get('PGSH_TOKEN', '')
    dl1 = os.environ.get('pg_dl', 'True').lower() == 'true'
    dl_url = os.environ.get('pg_dlurl', '')
    bf1 = os.environ.get('pg_bf', 'True').lower() == 'true'
    bfsum1 = int(os.environ.get('pg_bfsum', '5'))
    ts1 = os.environ.get('pg_ts', 'True').lower() == 'true'
    
    # 执行主要逻辑...
    """
    
    exec(script)

if __name__ == '__main__':
    app.run(debug=True) 
