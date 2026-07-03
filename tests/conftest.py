import pytest

from engine.game import Game


@pytest.fixture
def game() -> Game:
    return Game()