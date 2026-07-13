import requests
res = requests.post(
    "http://127.0.0.1:8001/items",
    json={"name": "ao", "price" : 1000, "description": "ao thun" },            
)
print(res.status_code)
print(res.text)