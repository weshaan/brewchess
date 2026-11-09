"""Admin configuration for the games application."""

from __future__ import annotations

from django.contrib import admin

from .models import ChessGame


@admin.register(ChessGame)
class ChessGameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "white_player",
        "black_player",
        "result",
        "variant",
        "event",
        "played_at",
        "created_at",
    )
    list_filter = ("result", "variant", "played_at")
    search_fields = ("white_player", "black_player", "event", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")
    autocomplete_fields = ("user",)
    date_hierarchy = "played_at"
    ordering = ("-played_at", "-created_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user",
                    "white_player",
                    "black_player",
                    "result",
                    "variant",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("played_at", "event", "site", "time_control"),
            },
        ),
        (
            "PGN",
            {
                "fields": ("pgn",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
