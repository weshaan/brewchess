"""Infrastructure API views for Brewchess."""

from __future__ import annotations

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Lightweight readiness probe for the API process."""

    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:
        return Response(
            {
                "status": "ok",
                "service": "brewchess-api",
            }
        )
