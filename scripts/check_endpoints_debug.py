import requests

API = "http://localhost:8001"

def check(endpoint, method="GET", **kwargs):
    url = f"{API}{endpoint}"
    try:
        if method == "GET":
            r = requests.get(url, **kwargs)
        else:
            r = requests.post(url, **kwargs)
        print(f"[{method}] {url} -> {r.status_code}")
        if r.status_code != 200:
            print(f"   Response: {r.text}")
    except Exception as e:
        print(f"[{method}] {url} -> FALHA DE CONEXÃO: {e}")

print("Verificando Endpoints...")
check("/")
check("/search?q=test")
check("/rag?q=test")
check("/api/index/list")
check("/api/index/create", method="POST", params={"name_index": "test-index"})
