import requests

data = {
    "username": "ananya",
    "password": "test123"
}

response = requests.post("http://127.0.0.1:5000/signup", json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
