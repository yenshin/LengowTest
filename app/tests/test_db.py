import pytest

from app.db.repository import Repository
from app.db.session import get_db
from app.domain.model_manager import DataManager


@pytest.fixture
def db_session():
    yield from get_db()


def test_filling_db():
    rep = Repository()
    dataMgr = DataManager()
    nbEntry = rep.count_dayli_reference()
    dataMgr.update_reference()
    dayliref = dataMgr.get_daily_ref()
    assert dayliref is not None

    rep.push_new_dayli_reference(dayliref)
    assert nbEntry + 1 == rep.count_dayli_reference()
