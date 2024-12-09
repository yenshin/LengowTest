import os
import sys

import typer

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)


from app.db.repository import Repository
from app.domain.model_manager import DataManager
from app.tools.logger import Logger, LogType


def main():
    dataMgr = DataManager()
    dataMgr.update_reference()
    repository = Repository()
    daylyref = dataMgr.get_daily_ref()
    if daylyref is not None:
        repository.push_new_dayli_reference(daylyref)
    else:
        Logger.push_log(LogType.ERROR, " update db script: can't add entry to the db")
    print("db updated")


if __name__ == "__main__":
    typer.run(main)
