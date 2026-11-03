# data types for pips puzzle

from dataclasses import dataclass
from typing import TypeAlias

Cell: TypeAlias = tuple[int, int]

# dataclass for dominoes
@dataclass(frozen=True)
class Domino:
    id: int
    pip1: int
    pip2: int

# dataclass for regions (shaded ares of puzzle with one rule)
@dataclass(frozen=True)
class Region:
    cells: frozenset[Cell]
    constraint_type: str
    target: int | None = None


# dataclass for the puzzle itself
@dataclass
class Puzzle:
    dominoes: list[Domino]
    regions: list[Region]
    cell_to_region: dict[Cell, Region]

# dataclass for a possible placement of a domino
@dataclass(frozen=True)
class Placement:
    domino_id: int
    cell1: Cell
    cell2: Cell
    pip1: int
    pip2: int


__all__ = [
    "Cell",
    "Domino",
    "Region",
    "Puzzle",
    "Placement"
]