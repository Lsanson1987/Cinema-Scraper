# Cinema-Scraper

A Python CLI tool that extracts structured cast metadata from IMDb using the
[Cinemagoer](https://cinemagoer.github.io/) library.

---

## Features

- Accepts any IMDb Film ID (e.g. `tt0111161` or `0111161`).
- Fetches the full cast list via Cinemagoer.
- For every cast member it reports:
  - Full Name
  - Character Name
  - Current Age (calculated from birth date)
  - Gender
- Displays the data in a clean tabular format in the terminal.
- Saves the data to a `cast_metadata.json` file (path is configurable).

---

## Requirements

- Python 3.10 or later
- [Cinemagoer](https://pypi.org/project/cinemagoer/)

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Lsanson1987/Cinema-Scraper.git
cd Cinema-Scraper

# 2. (Optional but recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py <imdb_id> [--output <file>]
```

| Argument | Description | Example |
|----------|-------------|---------|
| `imdb_id` | IMDb Film ID (**required**) | `tt0111161` |
| `--output` | Path for the JSON output file (optional, default: `cast_metadata.json`) | `--output shawshank.json` |

### Examples

```bash
# The Shawshank Redemption
python main.py tt0111161

# Inception – save output to a custom file
python main.py tt1375666 --output inception_cast.json

# Bare numeric ID also works
python main.py 0111161
```

### Sample output

```
Fetching cast data for IMDb ID tt0111161 …

+----------------------+------------------+-----+--------+
| Name                 | Character        | Age | Gender |
+----------------------+------------------+-----+--------+
| Tim Robbins          | Andy Dufresne    | 65  | male   |
| Morgan Freeman       | Ellis Boyd Redding | 87 | male   |
| ...                  | ...              | ... | ...    |
+----------------------+------------------+-----+--------+

Cast metadata saved to 'cast_metadata.json'.
```

---

## Output file

The tool writes a `cast_metadata.json` file (or a custom path via `--output`)
containing an array of objects like:

```json
[
  {
    "name": "Tim Robbins",
    "character": "Andy Dufresne",
    "age": 65,
    "gender": "male"
  },
  ...
]
```

Fields that are unavailable on IMDb are stored as `"N/A"`.

---

## Error handling

- **Invalid Film ID** – the script exits with an error message if the ID does
  not match the `tt<digits>` or `<digits>` format.
- **Movie not found** – a clear error is printed and the script exits with a
  non-zero code.
- **Missing age / gender** – stored as `"N/A"` in both the table and the JSON
  output.
