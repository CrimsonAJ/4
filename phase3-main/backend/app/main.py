from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.admin.router import router as admin_router

app = FastAPI(title="FastAPI Project", version="1.0.0")

# Mount static files and templates
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

# Create directories if they don't exist
os.makedirs(static_path, exist_ok=True)
os.makedirs(template_path, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=template_path)

# Include admin router
app.include_router(admin_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "FastAPI Project is running"}
