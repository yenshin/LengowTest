from app.api.schema.intput_query import InputQuery
from app.api.schema.output_answer import OutputAnswer


class _Parser:
    def __init__(self, input_query: InputQuery):
        self.__input_query = input_query

    def DoParse(self):
        return None


def ParseQuery(input_query: InputQuery):
    paser = _Parser(input_query)
    return paser.DoParse()
