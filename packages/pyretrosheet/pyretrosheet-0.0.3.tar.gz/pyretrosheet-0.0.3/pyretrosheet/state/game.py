"""Tracks a game's state as it plays out."""
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Optional

from pyretrosheet.models.game import ChronologicalEvent, Game
from pyretrosheet.models.play import Play
from pyretrosheet.models.player import Player
from pyretrosheet.models.team import TeamLocation
from pyretrosheet.state.base_state import BaseState


@dataclass
class TeamGameState:
    """Tracks variable state for a team over the course of a game.

    Args:
        players: players on the team
        batting_order_positions: map of batting position to player id
        fielding_positions: map of fielding position to player id
        inning_to_base_state: map of inning to base state
    """

    players: list[Player]
    batting_order_positions: dict[int, str]
    fielding_positions: dict[int, str]
    inning_to_base_state: dict[int, BaseState]

    @classmethod
    def from_game(cls, game: Game, team_location: TeamLocation) -> "TeamGameState":
        """Build a team's game state from a game.

        Args:
            game: the game to build the state for
            team_location: the team's location, home or away
        """
        players = []
        seen_player_ids = set()
        batting_order_positions = {}
        fielding_positions = {}
        inning_to_base_state = {}
        for event in game.chronological_events:
            if event.team_location != team_location:
                continue

            if isinstance(event, Player):
                player = event
                if player.id not in seen_player_ids:
                    players.append(player)
                    seen_player_ids.add(player.id)

                if not player.is_sub:
                    batting_order_positions[player.batting_order_position] = player.id
                    fielding_positions[player.fielding_position] = player.id
                else:
                    batting_subbed_player_id = _find_key_by_value(
                        batting_order_positions, player.batting_order_position
                    )
                    fielding_subbed_player_id = _find_key_by_value(fielding_positions, player.fielding_position)
                    if player.id != batting_subbed_player_id:
                        ...

                    if player.id != fielding_subbed_player_id:
                        ...

                    # TODO: switch lineup positions

            if isinstance(event, Play):
                play = event
                if play.inning not in inning_to_base_state:
                    inning_to_base_state[play.inning] = BaseState()

                base_state = inning_to_base_state[play.inning]
                base_state.update(play)

        return cls(
            players=players,
            batting_order_positions=batting_order_positions,
            fielding_positions=fielding_positions,
            inning_to_base_state=inning_to_base_state,
        )


@dataclass
class GameState:
    """@TODO."""

    bases: BaseState = field(default_factory=BaseState)

    def update(self, event: ChronologicalEvent, prev_state: Optional["GameState"]) -> None:
        """@TODO."""
        ...


def play_game(game: Game) -> Iterator[GameState]:
    """Iterate through a game and its state."""
    prev_state = None
    for event in game.chronological_events:
        game_state = GameState()
        game_state.update(event, prev_state)
        yield game_state
        prev_state = game_state


def _find_key_by_value(dict_: dict[Any, Any], value: Any) -> Any:
    """Find a dictionary's key by value.

    Note this function is stupid and assumes one valid solution exists.

    Args:
        dict_: the dictionary to lookup key
        value: the value to look for in the dictionary
    """
    return [k for k, v in dict_.items() if v == value][0]  # noqa: RUF015
