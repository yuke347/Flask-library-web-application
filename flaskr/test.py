import requests

base_url = 'http://127.0.0.1:5000/auth/register'
response = requests.post(base_url,data="test")
print(response,response.text)