from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.infrared_routes import router as api_router
from backend.api.routes.processing_routes import router as processing_router
from backend.api.routes.measurement_routes import router as measurement_router

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

app.include_router(processing_router, prefix="/process")

app.include_router(measurement_router, prefix="/measurements")