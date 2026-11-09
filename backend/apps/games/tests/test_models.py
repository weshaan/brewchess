"""Tests for the ChessGame model."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.games.models import ChessGame, ChessVariant, GameResult

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="player1",
        email="player1@example.com",
        password="secure-password-123",
    )


def _create_game(owner, **overrides) -> ChessGame:
    defaults = {
        "user": owner,
        "white_player": "Magnus Carlsen",
        "black_player": "Hikaru Nakamura",
        "result": GameResult.WHITE_WINS,
        "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 *",
    }
    defaults.update(overrides)
    return ChessGame.objects.create(**defaults)


@pytest.mark.django_db
def test_game_can_be_created(user) -> None:
    game = _create_game(user)

    assert game.pk is not None
    assert game.white_player == "Magnus Carlsen"
    assert game.black_player == "Hikaru Nakamura"


@pytest.mark.django_db
def test_game_belongs_to_specified_user(user) -> None:
    game = _create_game(user)

    assert game.user == user
    assert game.user_id == user.pk


@pytest.mark.django_db
def test_user_can_own_multiple_games(user) -> None:
    first = _create_game(user, white_player="Alice", black_player="Bob")
    second = _create_game(user, white_player="Carol", black_player="Dave", result=GameResult.DRAW)

    games = list(user.games.order_by("white_player"))

    assert len(games) == 2
    assert {game.pk for game in games} == {first.pk, second.pk}


@pytest.mark.django_db
def test_game_results_accept_supported_choices(user) -> None:
    for result in GameResult.values:
        game = _create_game(user, result=result)
        game.full_clean()
        assert game.result == result


@pytest.mark.django_db
def test_invalid_result_is_rejected_by_model_validation(user) -> None:
    game = ChessGame(
        user=user,
        white_player="Alice",
        black_player="Bob",
        result="2-0",
        pgn="1. e4 e5 *",
    )

    with pytest.raises(ValidationError) as exc_info:
        game.full_clean()

    assert "result" in exc_info.value.message_dict


@pytest.mark.django_db
def test_standard_chess_is_default_variant(user) -> None:
    game = _create_game(user)

    assert game.variant == ChessVariant.STANDARD
    assert game.variant == "standard"


@pytest.mark.django_db
def test_optional_metadata_can_be_omitted(user) -> None:
    game = _create_game(user)

    assert game.played_at is None
    assert game.event == ""
    assert game.site == ""
    assert game.time_control == ""


@pytest.mark.django_db
def test_optional_metadata_can_be_set(user) -> None:
    played_at = timezone.now()
    game = _create_game(
        user,
        played_at=played_at,
        event="Blitz Arena",
        site="Chess.com",
        time_control="180+2",
    )

    assert game.played_at == played_at
    assert game.event == "Blitz Arena"
    assert game.site == "Chess.com"
    assert game.time_control == "180+2"


@pytest.mark.django_db
def test_deleting_user_deletes_associated_games(user) -> None:
    game = _create_game(user)
    game_id = game.pk

    user.delete()

    assert not ChessGame.objects.filter(pk=game_id).exists()


@pytest.mark.django_db
def test_string_representation_is_readable(user) -> None:
    game = _create_game(
        user,
        white_player="White Hero",
        black_player="Black Hero",
        result=GameResult.DRAW,
    )

    assert str(game) == "White Hero vs Black Hero (1/2-1/2)"
