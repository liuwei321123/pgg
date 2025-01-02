from flask import Flask, render_template, request, jsonify
import time
import json
import requests
import hashlib
import random

app = Flask(__name__)

def generate_random_ua():
    brands = ['Xiaomi', 'HUAWEI', 'OPPO', 'vivo', 'Samsung', 'Redmi']
    models = ['Mi 10', 'P40', 'Find X3', 'X60', 'S21', 'Note 10']
    android_versions = ['10.0', '11.0', '12.0', '13.0']
    build_numbers = ['QKQ1.200114.002', 'RKQ1.200826.002', 'SKQ1.210216.001']
    
    brand = random.choice(brands)
    model = random.choice(models)
    android_version = random.choice(android_versions)
    build = random.choice(build_numbers)
    
    return f'Mozilla/5.0 (Linux; Android {android_version}; {brand} {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'

def sha256_encrypt(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

def signzfb(t, url, token):
    ls = sha256_encrypt('appSecret=Ew+ZSuppXZoA9YzBHgHmRvzt0Bw1CpwlQQtSl49QNhY=&channel=alipay&timestamp='+t+'&token='+token+'&version=1.59.3&'+url[25:])
    return ls

def sign(t, url, token):
    ls = sha256_encrypt('appSecret=nFU9pbG8YQoAe1kFh+E7eyrdlSLglwEJeA0wwHB1j5o=&channel=android_app&timestamp='+t+'&token='+token+'&version=1.59.3&'+url[25:])
    return ls

def process_task(token, ua):
    results = []
    try:
        # 签到任务
        url = 'https://userapi.qiekj.com/signin/signInAcList'
        t = str(int(time.time() * 1000))
        signs = sign(t, url, token)
        
        headers = {
            'Authorization': token,
            'Version': '1.59.3',
            'channel': 'android_app',
            'phoneBrand': 'Redmi',
            'timestamp': t,
            'sign': signs,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'userapi.qiekj.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': ua
        }
        
        data = {'token': token}
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        
        if result.get('code') == 0:
            results.append({'task': '签到', 'status': '成功'})
        else:
            results.append({'task': '签到', 'status': '失败', 'message': result.get('message', '未知错误')})
            
    except Exception as e:
        results.append({'task': '任务执行', 'status': '失败', 'message': str(e)})
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_task', methods=['POST'])
def run_task():
    try:
        tokens = request.form.get('tokens', '').strip()
        if not tokens:
            return jsonify({'status': 'error', 'message': '请输入token'})
        
        token_list = tokens.split('&')
        ua = generate_random_ua()
        all_results = []
        
        for tk in token_list:
            try:
                results = process_task(tk, ua)
                all_results.append({
                    'token': tk[:10] + '...',  # 只显示token的前10位
                    'results': results
                })
            except Exception as e:
                all_results.append({
                    'token': tk[:10] + '...',
                    'error': str(e)
                })
        
        return jsonify({
            'status': 'success',
            'results': all_results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
