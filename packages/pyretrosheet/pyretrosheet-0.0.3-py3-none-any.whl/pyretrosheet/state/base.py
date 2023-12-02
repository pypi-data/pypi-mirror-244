"""Tracks a game's base state as it plays out."""
from collections import defaultdict
from dataclasses import dataclass, field

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import Play

BaseStateMap = dict[Base, str | None]


class PlayerNotFoundOnBase(Exception):
    """Error when expecting a player on a base, but there is not."""

    def __init__(self, base: Base, state: BaseStateMap):
        """Initialize the exception.

        Args:
            base: the base the player is expected to be on
            state: the base state
        """
        super().__init__(f"Player not found on base: {base=} | {state=}")


class AdvancingPlayerToOccupiedBaseError(Exception):
    """Error when an advancing player is advancing to an already occupied base."""

    def __init__(self, player_id: str, to_base: Base, state: BaseStateMap):
        """Initialize the exception.

        Args:
            player_id: the player's id
            to_base: the base the player is attempting to advance to
            state: the base state
        """
        super().__init__(
            f"Attempted to advance player to a base already occupied: {player_id=} | {to_base=} | {state=}"
        )


class OutOnBaseWithoutPlayerError(Exception):
    """Error when attempting to out a base without a player on it."""

    def __init__(self, from_base: Base, state: BaseStateMap):
        """Initialize the exception.

        Args:
            from_base: the base the player is advancing from
            state: the base state
        """
        super().__init__(f"Attempted to out a runner on an unoccupied base: {from_base=} | {state=}")


@dataclass
class BaseState:
    """Tracks the base state within one half of an inning.

    Args:
         runs: map of player id to runs scored
         _state: internal state mapping bases to a player id or None
    """

    runs: defaultdict[str, int] = field(init=False)
    _state: BaseStateMap = field(init=False)

    def __post_init__(self):
        """Initialize empty bases."""
        self._state = {base: None for base in Base}
        self.runs = defaultdict(int)

    def update(self, play: Play) -> None:
        """Update the base state based on a play."""
        raise NotImplementedError()

    def _batter_advance(self, batter_id: str, to_base: Base) -> None:
        """Advance the batter to a base.

        Batters advancing to home are removed from the base state and added to runs.

        Args:
            batter_id: the batter's player id
            to_base: the base the player is going to
        """
        if to_base == Base.HOME:
            self.runs[batter_id] += 1

        self._raise_on_advancing_player_to_already_occupied_base(batter_id, to_base)
        self._state[to_base] = batter_id

    def _runner_advance(self, from_base: Base, to_base: Base) -> None:
        """Advance a runner from a base to another.

        Runners advancing to home are removed from the base state and added to runs.

        Args:
            from_base: the base the player is coming from
            to_base: the base the player is going to
        """
        player_id = self._state[from_base]
        if not player_id:
            raise PlayerNotFoundOnBase(from_base, self._state)

        if to_base == Base.HOME:
            self.runs[player_id] += 1
        else:
            self._raise_on_advancing_player_to_already_occupied_base(player_id, to_base)
            self._state[to_base] = player_id

        self._state[from_base] = None

    def _runner_out(self, from_base: Base) -> None:
        """Mark a runner out from a base, removing them from the base.

        Args:
            from_base: the base the player is coming from
        """
        try:
            del self._state[from_base]
        except KeyError as e:
            raise OutOnBaseWithoutPlayerError(from_base, self._state) from e

    def _raise_on_advancing_player_to_already_occupied_base(self, player_id: str, to_base: Base) -> None:
        """Raise in the case of a player attempting to advance to a base that is already occupied.

        Args:
            player_id: the player's id
            to_base: the base the player is going to
        """
        if self._state[to_base]:
            raise AdvancingPlayerToOccupiedBaseError(player_id, to_base, self._state)
