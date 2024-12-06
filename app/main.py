from fastapi import FastAPI

from app.api import add_app_routes
from app.domain import init_domain

app = FastAPI()
init_domain(app)
add_app_routes(app)
