import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.schema.intput_query import InputQuery
from app.api.schema.output_answer import OutputAnswer


@pytest.fixture
def api_app():
    from app.main import app

    return app


@pytest.fixture
def api_client(api_app):
    return TestClient(api_app)


def test_money_routes(api_client):
    # TEST missing query
    url = "/money/convert"
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # TEST not working query
    query = InputQuery(query="42")
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    query.query = "10.32 euros en dollars"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    original_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK

    query.query = "10.32 eurs = dollar"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert original_answer.answer == finded_answer.answer

    # multiple word currencies dest
    query.query = "10.32 eurs = dollar américains"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert original_answer.answer == finded_answer.answer

    # multiple word currencies src
    query.query = "10.32 euro européen = $"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert original_answer.answer == finded_answer.answer

    # no linker
    query.query = "10.32 eurs dollar américains"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    # multiple word currencies src and dest
    query.query = "10.32 euro européen = dollar américains"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert original_answer.answer == finded_answer.answer

    # multiple word currencies src and dest
    query.query = "10.32 euro européen = dollar amricains"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    query.query = "10.32 USD = USD"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert "10.32 USD = 10.32 USD" == finded_answer.answer

    query.query = "10.3285146196 jpy = jpy"
    response = api_client.post(
        url,
        json=json.loads(query.model_dump_json()),
    )
    finded_answer = OutputAnswer.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    # INFO: 10.328 => 10.33
    # and also all code are in upper case even for input
    assert "10.3285146196 JPY = 10.33 JPY" == finded_answer.answer
