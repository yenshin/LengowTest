import json
import uuid
from dataclasses import dataclass
from locale import currency

from sqlalchemy import Date, cast
from sqlmodel import desc

from app.db.model.currency_rate import CurrencyRate as db_curate
from app.db.model.daily_reference import DailyReference as db_dayref
from app.db.session import get_db
from app.domain.model.currency_rate import CurrencyRate as dom_curate
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
            db_ref = db_dayref(
                # INFO: use uuid1 to order by date and hostname
                id=uuid.uuid1(),
                date=cast(input_val.date, Date),
            )
            session.add(db_ref)
            session.flush()
            for key in input_val.currencies:
                name: str = key
                rate: float = input_val.currencies[key].rate
                curate = db_curate(
                    id=uuid.uuid4(),
                    dailyref_id=db_ref.id,
                    currency_type=name,
                    currency_rate=rate,
                )
                session.add(curate)
                session.flush()
            session.commit()
            toReturn = True
        except Exception as e:
            session.rollback()
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
            currlist = (
                session.query(db_curate).where(db_curate.dailyref_id == dbmod.id).all()
            )

            session.commit()
            toReturn = dom_dayref(date=dbmod.date, currencies={})
            for curr in currlist:
                toReturn.currencies[curr.currency_type] = dom_curate(
                    currency=curr.currency_type,
                    rate=curr.currency_rate,
                )

        except Exception as e:
            session.rollback()
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
            session.rollback()
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
