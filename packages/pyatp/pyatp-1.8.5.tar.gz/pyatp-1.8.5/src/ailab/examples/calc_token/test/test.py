import requests

# Flask 服务的地址
flask_url = "http://localhost:5001"

# 发送 POST 请求
data = {"dataset_path": "/home/sdk_dataset/ailabsdk_dataset/nlp/alpaca/alpaca_data_chinese_51k/alpaca_data_zh_51k.json",
        "token_path" : "/home/sdk_models/chinese_llama_alpaca_2"}
response_post = requests.post(f"{flask_url}/calc_tokens", json=data)

# 处理响应
print("POST Response:")
print(f"Status Code: {response_post.status_code}")
print(f"Content: {response_post.json()}")
