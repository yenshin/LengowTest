from fastapi import APIRouter, Response, status

from app.api.schema import schema_const
from app.api.schema.intput_query import InputQuery
from app.api.schema.output_answer import OutputAnswer
from app.domain.model_manager import DataManager
from app.domain.parser import parse_query

router = APIRouter()


def __checkResponse(outputStr: str | None, response: Response) -> OutputAnswer:
    if outputStr is None:
        # INFO: the normal way to handle error should be this
        # raise HTTPException(
        #     status_code=500,
        #     detail=schema_const.OUTPUT_DEFAULTANSWER,
        # )
        # https://fastapi.tiangolo.com/tutorial/handling-errors/#requestvalidationerror-vs-validationerror
        # but because of the specific requestion from the instruction I set
        # the response myself
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        outputStr = schema_const.OUTPUT_DEFAULTANSWER
    return OutputAnswer(answer=outputStr)


# INFO: in the exercice it's written: "Il sera appelable en JSON via la méthode GET"
# and in the proposed exemple it used post method
#
# I choose Post moethod only to simplify the exercice, and also because
# get with a json payload as requested isn't recommended
@router.post("/convert")
async def convert_money(input_query: InputQuery, response: Response) -> OutputAnswer:
    # INFO: is input_query is not set default fastapi answer is 422
    # no information provided to adapt this error code
    # just 200 if query is ok or 500 if query no understanble
    datamanager = DataManager()
    currencies = datamanager.get_currencies()
    value = None
    if currencies is not None:
        value = parse_query(input_query.query, currencies)
    return __checkResponse(value, response)
