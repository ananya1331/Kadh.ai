import requests

BASE_URL = "http://127.0.0.1:5000"

# Use valid user_id and recipe_id
user_id = 1
recipe_id = 2

# ----------------- Add Review -----------------
review_data = {
    "user_id": user_id,
    "recipe_id": recipe_id,
    "review": "Delicious and easy to make!"
}
response = requests.post(f"{BASE_URL}/review", json=review_data)
print("Add Review - Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("No JSON response")

# ----------------- Get Reviews -----------------
response = requests.get(f"{BASE_URL}/reviews/{recipe_id}")
print("\nGet Reviews - Status Code:", response.status_code)
try:
    print("Reviews:", response.json())
except Exception:
    print("No JSON response")
