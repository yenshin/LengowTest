from fastapi import FastAPI

from app.api import add_app_routes
from app.config.config import settings
from app.domain import init_domain

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)
init_domain(app)
add_app_routes(app)
