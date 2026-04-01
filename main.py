"""Cinema Scraper – CLI tool to extract cast metadata from IMDb via Cinemagoer."""

import argparse
import json
import re
import sys
from datetime import date, datetime

from imdb import Cinemagoer, IMDbDataAccessError


def parse_imdb_id(raw_id: str) -> str:
    """Normalise an IMDb ID to a bare numeric string (e.g. 'tt0111161' → '0111161')."""
    raw_id = raw_id.strip()
    match = re.fullmatch(r"tt(\d+)", raw_id, re.IGNORECASE)
    if match:
        return match.group(1)
    if re.fullmatch(r"\d+", raw_id):
        return raw_id
    raise ValueError(
        f"Invalid IMDb Film ID '{raw_id}'. "
        "Please provide an ID in the format 'tt1234567' or '1234567'."
    )


def calculate_age(birth_date_str: str) -> int | None:
    """Return current age in years given a birth-date string, or None if unparseable."""
    for fmt in ("%Y-%m-%d", "%d %b %Y", "%b %d, %Y", "%Y"):
        try:
            bdate = date.fromisoformat(birth_date_str) if fmt == "%Y-%m-%d" else None
            if bdate is None:
                bdate = datetime.strptime(birth_date_str, fmt).date()
            today = date.today()
            return (
                today.year
                - bdate.year
                - ((today.month, today.day) < (bdate.month, bdate.day))
            )
        except (ValueError, AttributeError):
            continue
    return None


def fetch_cast_metadata(movie_id: str) -> list[dict]:
    """Fetch cast metadata for the given numeric IMDb movie ID."""
    ia = Cinemagoer()
    try:
        movie = ia.get_movie(movie_id)
    except IMDbDataAccessError as exc:
        print(f"Error: Could not retrieve movie data – {exc}", file=sys.stderr)
        sys.exit(1)

    if not movie:
        print(f"Error: No movie found for ID 'tt{movie_id}'.", file=sys.stderr)
        sys.exit(1)

    cast = movie.get("cast", [])
    if not cast:
        print("Warning: No cast information available for this title.", file=sys.stderr)
        return []

    records = []
    for person in cast:
        # Fetch full person details to obtain bio data (birth date, gender).
        try:
            ia.update(person, info=["biography"])
        except (IMDbDataAccessError, Exception):  # noqa: BLE001
            print(
                f"Warning: Could not retrieve biography for '{person.get('name', '?')}'.",
                file=sys.stderr,
            )

        name: str = person.get("name", "N/A")

        # Character name – stored under the person's currentRole attribute.
        role = person.currentRole
        if hasattr(role, "__iter__") and not isinstance(role, str):
            # Multiple roles → join them
            character = " / ".join(str(r) for r in role) or "N/A"
        else:
            character = str(role) if role else "N/A"

        # Birth date / age
        birth_date_str: str = person.get("birth date", "") or ""
        age = calculate_age(birth_date_str) if birth_date_str else None

        # Gender
        gender: str | None = person.get("gender", None)

        records.append(
            {
                "name": name,
                "character": character,
                "age": age if age is not None else "N/A",
                "gender": gender if gender else "N/A",
            }
        )

    return records


def print_table(records: list[dict]) -> None:
    """Print cast records in a formatted table to stdout."""
    if not records:
        print("No cast data to display.")
        return

    headers = ["Name", "Character", "Age", "Gender"]
    col_keys = ["name", "character", "age", "gender"]

    # Compute column widths
    widths = [len(h) for h in headers]
    for rec in records:
        for i, key in enumerate(col_keys):
            widths[i] = max(widths[i], len(str(rec[key])))

    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    row_fmt = "|" + "|".join(f" {{:<{w}}} " for w in widths) + "|"

    print(sep)
    print(row_fmt.format(*headers))
    print(sep)
    for rec in records:
        print(row_fmt.format(*(str(rec[k]) for k in col_keys)))
    print(sep)


def save_json(records: list[dict], path: str = "cast_metadata.json") -> None:
    """Serialise records to a JSON file."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)
    print(f"\nCast metadata saved to '{path}'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cinema-scraper",
        description="Extract structured cast metadata from IMDb using Cinemagoer.",
    )
    parser.add_argument(
        "imdb_id",
        help="IMDb Film ID (e.g. tt0111161 or 0111161)",
    )
    parser.add_argument(
        "--output",
        default="cast_metadata.json",
        metavar="FILE",
        help="Path for the output JSON file (default: cast_metadata.json)",
    )
    args = parser.parse_args()

    try:
        movie_id = parse_imdb_id(args.imdb_id)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching cast data for IMDb ID tt{movie_id} …\n")
    records = fetch_cast_metadata(movie_id)

    if records:
        print_table(records)
        save_json(records, args.output)
    else:
        print("No cast records found.")


if __name__ == "__main__":
    main()
