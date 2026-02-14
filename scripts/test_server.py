from fastapi import FastAPI
import uvicorn
import sys

# Ensure current directory is in path
sys.path.append(".")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    print("Starting minimal server on 8001...")
    uvicorn.run("test_server:app", host="127.0.0.1", port=8001, log_level="info")
