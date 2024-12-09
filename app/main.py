from fastapi import FastAPI

import app.db.repository as rp
from app.api import add_app_routes
from app.config.config import settings
from app.domain import init_domain
from app.tools.logger import Logger, LogType

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

init_domain(app)
add_app_routes(app)
# initialize domain data
if rp.initialize_domaindata_from_repository() is False:
    if rp.initialize_repository_and_domaindata_from_refsite is False:
        errMsg = "cant init DOMAIN from the db or the ref site"
        Logger.push_log(LogType.ERROR, errMsg)
        Exception(errMsg)
