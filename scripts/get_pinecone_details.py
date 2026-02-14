import requests
import json

API = "http://localhost:8001"

print("Listing indexes...")
try:
    r = requests.get(f"{API}/api/index/list")
    if r.status_code == 200:
        indexes = r.json()
        print(f"Indexes found: {json.dumps(indexes, indent=2)}")
        
        target_index = None
        if isinstance(indexes, dict) and 'indexes' in indexes:
             if len(indexes['indexes']) > 0:
                target_index = indexes['indexes'][0]['name']
        elif isinstance(indexes, list) and len(indexes) > 0:
             target_index = indexes[0]['name']

        if target_index:
            print(f"\nGetting details for index: {target_index}")
            r_detail = requests.post(f"{API}/api/index/detail", params={"name_index": target_index})
            if r_detail.status_code == 200:
                print("Details:")
                print(json.dumps(r_detail.json(), indent=2))
            else:
                print(f"Error getting details: {r_detail.status_code} - {r_detail.text}")
        else:
            print("No index found to get details from.")
            
    else:
        print(f"Error listing indexes: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Exception: {e}")
