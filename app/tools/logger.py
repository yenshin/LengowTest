import enum
import inspect
import os
import sys
import uuid as uid
from dataclasses import dataclass


class LogType(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICALSECURITY = "CRITICALSECURITY"


@dataclass
class LogModel:
    __tablename__ = "logs"
    uuid: uid.UUID
    log_type: LogType
    prefix: str
    msg: str
    additionnal_info: str

    def ToString(self):
        return str(self.ToDict())

    def __repr__(self):
        return self.ToString()

    def ToDict(self):
        dict = {}
        dict["log_type"] = self.log_type
        dict["prefix"] = self.prefix
        dict["msg"] = self.msg
        dict["additionnal_info"] = self.additionnal_info
        return dict


class Logger:
    @staticmethod
    def __GeneratePrefix():
        prefix = ""
        frame = sys._getframe().f_back
        if frame is None:
            prefix = "unknown[?: ?]"
        else:
            # we went the caller func
            frame = frame.f_back
            if frame is None:
                prefix = "unknown[?: ?]"
            else:
                info = inspect.getframeinfo(frame)
                funcName = info.function
                fileName = os.path.basename(info.filename)
                lineNumber = info.lineno
                prefix = "%s[%s: %s]" % (str(fileName), str(funcName), str(lineNumber))
        return prefix

    @staticmethod
    def GenerateLog(logType: LogType, msg: str, additionnalInfo: str = "") -> LogModel:
        prefix = Logger.__GeneratePrefix()
        logModel = LogModel(
            # INFO: uuid1 is not fully random and use timestand and host id
            # convenient for logs other things like that
            uuid=uid.uuid1(),
            log_type=logType,
            prefix=prefix,
            msg=msg,
            additionnal_info=additionnalInfo,
        )
        return logModel

    @staticmethod
    def push_log(type: LogType, msg: str, additionnalInfo: str = ""):
        log = Logger.GenerateLog(type, msg, additionnalInfo)
        print(log)
