"""
Main Entrypoint — Kashmir Mountain Operations FastAPI Service
=============================================================
Run:
    python main.py
Or:
    uvicorn main:app --reload --port 8000
"""

import uvicorn
from fastapi_intro_lab import app

if __name__ == "__main__":
    print("\n" + "=" * 78)
    print("🏔️  Starting Kashmir Mountain Operations API with Uvicorn ASGI Server...")
    print("=" * 78)
    print("📍 Interactive Swagger UI : http://127.0.0.1:8000/docs")
    print("📖 Interactive ReDoc UI   : http://127.0.0.1:8000/redoc")
    print("📜 Raw OpenAPI Schema     : http://127.0.0.1:8000/openapi.json")
    print("=" * 78 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

