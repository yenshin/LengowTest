from app.domain.model_manager import DataManager


def init_domain(app):
    dm = DataManager()
    dm.Log()
