import pytest

from lazy_flask import App


@pytest.fixture(autouse=True)
def app_client():
    # ensure clean singleton between tests using reset helper
    App.reset()
    app = App()
    client = app.test_client()
    return app, client


def test_non_json_content_type_returns_400(app_client):
    _, client = app_client
    resp = client.post(
        "/query", data="not json", headers={"Content-Type": "text/plain"}
    )
    assert resp.status_code == 400
    payload = resp.get_json()
    assert payload is not None
    assert payload.get("error", {}).get("code") == 400


def test_invalid_json_body_returns_400(app_client):
    _, client = app_client
    # invalid json body
    resp = client.post("/query", data="{", headers={"Content-Type": "application/json"})
    assert resp.status_code == 400
    payload = resp.get_json()
    assert payload is not None
    assert payload.get("error", {}).get("code") == 400
