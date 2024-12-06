from fastapi import APIRouter, Response, status

from app.api.schema import schema_const
from app.api.schema.intput_query import InputQuery
from app.api.schema.output_answer import OutputAnswer
from app.domain.parser import ParseQuery

router = APIRouter()


def __checkResponse(output: OutputAnswer | None, response: Response):
    if output is None:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        output = OutputAnswer(answer=schema_const.OUTPUT_DEFAULTANSWER)
    return output


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
    value = __checkResponse(ParseQuery(input_query), response)
    return value
