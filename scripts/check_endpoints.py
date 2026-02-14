import requests
import sys

def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"Checking {url}: Status {response.status_code}")
        if response.status_code == 200:
            print(f"Content snippet: {response.text[:100]}")
    except Exception as e:
        print(f"Error checking {url}: {e}")

if __name__ == "__main__":
    print("\n--- Checking Port 8000 (Main App) ---")
    check_url("http://127.0.0.1:8000/")
    check_url("http://127.0.0.1:8000/docs")
    # check_url("http://127.0.0.1:8000/search?q=test") # Validation
