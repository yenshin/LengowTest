from app.api import money


def add_app_routes(app):
    app.include_router(money.router, prefix="/money", tags=["Money"])
