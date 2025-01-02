import time
import json
import requests
import hashlib
import random

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
    
    ua = f'Mozilla/5.0 (Linux; Android {android_version}; {brand} {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'
    return ua

# 获取用户输入的tokens
print("请输入账号token(多个账号用&分隔)：")
tokens = input().strip()
token = tokens.split("&")
ua = generate_random_ua()

# 其余代码保持不变... 