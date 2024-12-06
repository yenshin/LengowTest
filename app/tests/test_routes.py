import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.schema.intput_query import InputQuery


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
