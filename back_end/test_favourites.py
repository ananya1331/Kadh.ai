import requests

BASE_URL = "http://127.0.0.1:5000"

# Replace with the actual user_id from your signup/login response
user_id = 1  
recipe_id = 2  # Replace with a valid recipe ID from your dummy data

# ----------------- Add Favorite -----------------
add_data = {
    "user_id": user_id,
    "recipe_id": recipe_id
}
response = requests.post(f"{BASE_URL}/favorites", json=add_data)
print("Add Favorite - Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("No JSON response")

# ----------------- Get Favorites -----------------
response = requests.get(f"{BASE_URL}/favorites/{user_id}")
print("\nGet Favorites - Status Code:", response.status_code)
try:
    print("Favorites:", response.json())
except Exception:
    print("No JSON response")
