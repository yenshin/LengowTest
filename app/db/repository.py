import json
import uuid
from dataclasses import dataclass

from sqlalchemy import Date, cast
from sqlmodel import desc

from app.db.model.conversion import DailyReference as db_dayref
from app.db.session import get_db
from app.domain.model.daily_reference import DailyReference as dom_dayref
from app.domain.model_manager import DataManager
from app.tools.logger import Logger, LogType
from app.tools.singleton import Singleton


@dataclass
class Repository(metaclass=Singleton):
    def push_new_dayli_reference(self, input_val: dom_dayref) -> bool:
        toReturn = False
        try:
            session = next(get_db())
            jsondata = json.dumps(input_val.currencies, default=vars)
            db_ref = db_dayref(
                # INFO: use uuid1 to order by date and hostname
                id=uuid.uuid1(),
                date=cast(input_val.date, Date),
                currencies=jsondata,
            )
            session.add(db_ref)
            session.flush()
            session.commit()
            toReturn = True
        except Exception as e:
            additionnalInfo: str = str(e)
            # INFO: no clever message
            Logger.push_log(
                LogType.ERROR, "failed to add new daily ref", additionnalInfo
            )
        finally:
            return toReturn

    def get_last_dayli_reference(self) -> dom_dayref | None:
        toReturn = None
        try:
            session = next(get_db())
            dbmod: dom_dayref = (
                session.query(db_dayref).order_by(desc(db_dayref.id)).first()
            )
            session.commit()
            toReturn = dbmod.GetDomainModel()
        except Exception as e:
            additionnalInfo: str = str(e)
            # INFO: no clever message
            Logger.push_log(
                LogType.ERROR, "failed to get last daily ref", additionnalInfo
            )
        finally:
            return toReturn

    def count_dayli_reference(self) -> int:
        toReturn = 0
        try:
            session = next(get_db())
            toReturn = session.query(db_dayref.id).count()
            session.commit()
        except Exception as e:
            toReturn = 0
            additionnalInfo: str = str(e)
            # INFO: no clever message
            Logger.push_log(LogType.ERROR, "count failed", additionnalInfo)
        finally:
            return toReturn


def initialize_domaindata_from_repository() -> bool:
    repository = Repository()
    datamanager = DataManager()
    tmpdata = repository.get_last_dayli_reference()
    if tmpdata is not None:
        datamanager.initialize_from_outside(tmpdata)
        return True
    return False


def initialize_repository_and_domaindata_from_refsite() -> bool:
    datamanager = DataManager()
    repository = Repository()
    datamanager.update_reference()
    dayliref = datamanager.get_daily_ref()
    if dayliref is not None:
        repository.push_new_dayli_reference(dayliref)
        return True
    return False
