from src.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run("run:app", port=8000, reload=True)