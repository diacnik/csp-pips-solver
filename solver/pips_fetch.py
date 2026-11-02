# python script to fetch pip puzzles from API
import json
import os
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://jindrich-bar--nyt-games-api.apify.actor"

def get_pips_puzzle(
        puzzle_date: date | None = None,
        *,
        token: str | None = None,
) -> dict[str, Any]:
    api_token = token or os.environ.get("APIFY_TOKEN")
    if not api_token:
        raise ValueError("APIFY token not provided")

    # api request url
    # build endpoint
    endpoint = "/pips"
    if puzzle_date is not None:
        endpoint += f"/{puzzle_date.isoformat()}"
    # build request url
    url = f"{API_URL}{endpoint}?{urlencode({'token': api_token})}"
    request = Request(url, headers={"Accept": "application/json"})

    # make api request
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Pips API returned HTTP {error.code}: {body}") from error
    except URLError as error:
        raise RuntimeError(f"Pips API returned URL {error.reason}") from error

    return payload

# save the puzzle as json
def save_pips_puzzle(puzzle: dict[str, Any], path: str) -> None:
    fixture_path = Path(path)
    fixture_path.parent.mkdir(parents=True, exist_ok=True)
    fixture_path.write_text(json.dumps(puzzle, indent=2) + "/n", encoding="utf-8")

# load puzzle
def load_pips_puzzle(path: str | Path) -> dict[str, Any]:
    fixture_path = Path(path)
    try:
        puzzle = json.loads(fixture_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Pips puzzle fixture does not exist: {fixture_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Pips fixture must contain a JSON object: {fixture_path}") from error

    return puzzle

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch or load a Pips puzzle.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--save",
        metavar="PATH",
        help="fetch today's puzzle and save it as a JSON fixture",
    )
    source.add_argument(
        "--load",
        metavar="PATH",
        help="load a previously saved JSON fixture instead of calling the API",
    )
    args = parser.parse_args()

    puzzle = load_pips_puzzle(args.load) if args.load else get_pips_puzzle()
    if args.save:
        save_pips_puzzle(puzzle, args.save)
    print(json.dumps(puzzle, indent=2))