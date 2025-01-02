from flask import Flask, render_template, request, jsonify
import time
import json
import requests
import hashlib
import random

app = Flask(__name__)

def generate_random_ua():
    # 常见的Android手机品牌和型号
    brands = ['Xiaomi', 'HUAWEI', 'OPPO', 'vivo', 'Samsung', 'Redmi']
    models = ['Mi 10', 'P40', 'Find X3', 'X60', 'S21', 'Note 10']
    android_versions = ['10.0', '11.0', '12.0', '13.0']
    build_numbers = ['QKQ1.200114.002', 'RKQ1.200826.002', 'SKQ1.210216.001']
    
    brand = random.choice(brands)
    model = random.choice(models)
    android_version = random.choice(android_versions)
    build = random.choice(build_numbers)
    
    return f'Mozilla/5.0 (Linux; Android {android_version}; {brand} {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'

# 将原有的功能函数保持不变，只是移除print语句，改为返回结果字符串
def sha256_encrypt(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

# ... (其他原有函数保持不变，但修改print为返回字符串)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_task', methods=['POST'])
def run_task():
    tokens = request.form.get('tokens', '').strip()
    if not tokens:
        return jsonify({'status': 'error', 'message': '请输入token'})
    
    token_list = tokens.split('&')
    ua = generate_random_ua()
    results = []
    
    for tk in token_list:
        try:
            # 执行原有的任务逻辑，但将print改为收集结果
            result = {}
            # ... (执行原有的任务逻辑)
            results.append(result)
        except Exception as e:
            results.append({'status': 'error', 'message': str(e)})
    
    return jsonify({'status': 'success', 'results': results})

if __name__ == '__main__':
    app.run(debug=True) 