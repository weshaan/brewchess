"""Chess game models for Brewchess."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class GameResult(models.TextChoices):
    WHITE_WINS = "1-0", "White won"
    BLACK_WINS = "0-1", "Black won"
    DRAW = "1/2-1/2", "Draw"
    UNKNOWN = "*", "Unknown or unfinished"


class ChessVariant(models.TextChoices):
    STANDARD = "standard", "Standard chess"


class ChessGame(models.Model):
    """A chess game owned by a user, typically imported from PGN."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games",
    )
    white_player = models.CharField(max_length=100)
    black_player = models.CharField(max_length=100)
    result = models.CharField(
        max_length=7,
        choices=GameResult.choices,
        default=GameResult.UNKNOWN,
    )
    pgn = models.TextField()
    played_at = models.DateTimeField(null=True, blank=True)
    event = models.CharField(max_length=255, blank=True, default="")
    site = models.CharField(max_length=255, blank=True, default="")
    time_control = models.CharField(max_length=64, blank=True, default="")
    variant = models.CharField(
        max_length=32,
        choices=ChessVariant.choices,
        default=ChessVariant.STANDARD,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-played_at", "-created_at"]
        indexes = [
            models.Index(fields=["user", "-played_at"], name="games_user_played_at_idx"),
            models.Index(fields=["user", "-created_at"], name="games_user_created_at_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.white_player} vs {self.black_player} ({self.result})"

    def clean(self) -> None:
        super().clean()
        valid_results = {choice.value for choice in GameResult}
        if self.result not in valid_results:
            raise ValidationError({"result": f"'{self.result}' is not a supported game result."})
