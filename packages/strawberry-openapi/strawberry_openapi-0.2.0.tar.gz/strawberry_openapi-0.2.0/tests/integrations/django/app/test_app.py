from __future__ import annotations

from django.test import Client


def test_404(client: Client):
    response = client.get("/hello")

    assert response.status_code == 404


def test_get(client: Client):
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"user": {"id": "1"}}


def test_delete(client: Client):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {"deleteUser": True}
