from pydantic import BaseModel


class OutputAnswer(BaseModel):
    answer: str = ""
