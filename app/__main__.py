import uvicorn
from app.main import make_app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:make_app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        factory=True,
        access_log=False
    )
