"""Tests for the API health check endpoint."""

from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def test_health_endpoint_returns_200(api_client: APIClient) -> None:
    response = api_client.get(reverse("health-check"))

    assert response.status_code == status.HTTP_200_OK


def test_health_endpoint_returns_json(api_client: APIClient) -> None:
    response = api_client.get(reverse("health-check"))

    assert response["Content-Type"].startswith("application/json")
    assert isinstance(response.json(), dict)


def test_health_endpoint_status_is_ok(api_client: APIClient) -> None:
    response = api_client.get(reverse("health-check"))

    assert response.json()["status"] == "ok"


def test_health_endpoint_service_name(api_client: APIClient) -> None:
    response = api_client.get(reverse("health-check"))

    assert response.json()["service"] == "brewchess-api"


def test_unknown_api_url_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/does-not-exist/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
