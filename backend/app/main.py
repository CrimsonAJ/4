from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.admin.router import router as admin_router
from app.proxy.router import router as proxy_router
from app.config import settings

app = FastAPI(title="ProxiBase", version="1.0.0")

# Mount static files and templates
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

# Create directories if they don't exist
os.makedirs(static_path, exist_ok=True)
os.makedirs(template_path, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=template_path)


# Health check - must be before routers
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Root endpoint - only for admin host
@app.get("/")
async def root(request: Request):
    host = request.headers.get('host', '')
    if host == settings.ADMIN_HOST or host.startswith('0.0.0.0') or host.startswith('localhost'):
        return {"message": "ProxiBase is running"}
    # For other hosts, let proxy handle it
    return Response(status_code=404)


# Include admin router (handles /admin, /login, /logout paths)
app.include_router(admin_router)

# Include proxy router last (catch-all for mirror domains)
app.include_router(proxy_router)
