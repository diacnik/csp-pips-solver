# parses the json puzzle and converts into typed objects

from __future__ import annotations

from pathlib import Path
from typing import Any

from pips_fetch import load_pips_puzzle
from puzzle_types import Cell, Domino, Puzzle, Region

_Constraints = {"sum", "less", "greater", "equals", "unequals", "empty"}
_PIP_MIN = 0
_PIP_MAX = 6

# load and parse puzzle from saved Pips puzzle
# easy difficulty is hardcoded
def parse_pips_puzzle(path: str | Path) -> Puzzle:
    puzzle_data = load_pips_puzzle(path)

    try:
        easy_data = puzzle_data["easy"]
        raw_dominoes = easy_data["dominoes"]
        raw_regions = easy_data["regions"]
    except KeyError as error:
        raise ValueError(f"required field missing: {error.args[0]}") from error
    except TypeError as error:
        raise ValueError("puzzle not an object") from error

    dominoes = parse_dominoes(raw_dominoes)
    regions, cell_to_region = parse_regions(raw_regions)

    return Puzzle(
        dominoes=dominoes,
        regions=regions,
        cell_to_region=cell_to_region,
    )

def parse_dominoes(raw_dominoes: Any) -> list[Domino]:
    dominoes: list[Domino] = []

    for domino_id, raw_domino in enumerate(raw_dominoes):
       pip1, pip2 = raw_domino
       dominoes.append(Domino(domino_id, pip1, pip2))

    return dominoes

def parse_regions(raw_regions: Any) -> tuple[list[Region], dict[Cell, Region]]:
    regions: list[Region] = []
    cell_to_region: dict[Cell, Region] = {}
    for region_id, raw_region in enumerate(raw_regions):
        raw_indices = raw_region["indices"]
        constraint_type = raw_region["type"]

        cells = frozenset(parse_cell(raw_cell) for raw_cell in raw_indices)
        target = raw_region.get("target")

        region = Region(cells, constraint_type, target)
        regions.append(region)
        for cell in cells:
            cell_to_region[cell] = region

    return regions, cell_to_region

def parse_cell(raw_cell: Any) -> Cell:
    return raw_cell[0], raw_cell[1]
