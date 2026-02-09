#!/usr/bin/env python3
"""Basic endpoint checks that run inside pytest without a live server."""

from fastapi.testclient import TestClient

from app.main import app


def test_all_endpoints():
    client = TestClient(app)

    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json() == {"message": "Hello World"}

    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}

