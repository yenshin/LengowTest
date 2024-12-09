import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict

import requests

from app.domain import domain_const
from app.domain.model.currency_rate import CurrencyRate
from app.domain.model.daily_reference import DailyReference
from app.tools.logger import Logger, LogType
from app.tools.singleton import Singleton

# INFO: this class aim to single entry point to access data


class DataManager(metaclass=Singleton):
    # INFO: here we use a single obj
    #
    # we could use an dict(date, DailyReference)
    # if server is runnning for more than one day with
    # job scheduling to automaticly update
    # this could be a thing
    #
    # or maybe we could go for a dedicated service if this is a strong need
    # with frequent data update
    # => because it's job interview I need to limit my work
    __daily_refs: DailyReference | None = None

    def update_reference(self):
        response = requests.get(domain_const.REF_URLCONVERSION)
        xmlRoot = ET.fromstring(response.content)
        currDict: Dict[str, CurrencyRate] = {}
        namespaces = {
            domain_const.REF_XMLNAMESPACE_PREFIX: domain_const.REF_XMLNAMESPACE_URL
        }
        match = xmlRoot.find(domain_const.REF_XMLDATE_QUERY, namespaces=namespaces)
        if match is None:
            raise Exception("no date found")

        match.attrib[domain_const.REF_XMLCURRENCY_KDATE]
        documentDate = datetime.strptime(
            match.attrib[domain_const.REF_XMLCURRENCY_KDATE], "%Y-%m-%d"
        ).date()
        for cube in xmlRoot.findall(
            domain_const.REF_XMLCURRENCIES_QUERY, namespaces=namespaces
        ):
            key = cube.attrib[domain_const.REF_XMLCURRENCY_KNAME]
            value = cube.attrib[domain_const.REF_XMLCURRENCY_KRATE]
            currDict[key] = CurrencyRate(key, float(value))
        # INFO: to simplify utilisation I add eur
        if "EUR" not in currDict:
            currDict["EUR"] = CurrencyRate("EUR", 1.0)

        # INFO: add a new entry to the data
        self.__daily_refs = DailyReference(documentDate, currDict)

    def initialize_from_outside(self, input: DailyReference):
        self.__daily_refs = input

    def log(self):
        Logger.push_log(LogType.INFO, str(self.__daily_refs))

    def get_daily_ref(self) -> DailyReference | None:
        return self.__daily_refs

    def get_currencies(self) -> Dict[str, CurrencyRate]:
        return self.__daily_refs.currencies
