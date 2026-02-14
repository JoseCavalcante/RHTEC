
import requests
import sys

try:
    print("Testing /search endpoint...")
    r = requests.get("http://localhost:8001/search", params={"q": "desenvolvedor python"})
    print(f"Status Code: {r.status_code}")
    if r.status_code != 200:
        print(f"Response Text: {r.text}")
    else:
        print("Success!")
        data = r.json()
        print(f"Results: {len(data)}")
        if len(data) > 0:
            print("First result sample:", data[0])
            
except Exception as e:
    print(f"Request failed: {e}")
