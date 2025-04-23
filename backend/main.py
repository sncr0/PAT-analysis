from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or "*" for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global landing endpoint
@app.get("/")
def landing():
    return {
        "message": "📡 Welcome to the Spectroscopy Platform",
        "routes": {
            "/api/": "All API endpoints",
            "/api/infrared/all": "Preview all stored infrared measurements",
            "/docs": "Interactive API documentation",
            "/redoc": "Alternative API docs"
        }
    }


app.include_router(api_router, prefix="/api")
