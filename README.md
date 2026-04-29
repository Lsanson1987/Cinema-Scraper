# Cinema-Scraper: Dual-Method IMDb Metadata Extraction

A professional-grade Python tool designed to extract structured cast and crew metadata directly from IMDb. This project employs a sophisticated dual-method architecture to navigate modern web security challenges, utilizing both live web scraping and official IMDb database processing.

---

Aryamaan Goswamy (**goswamy4**) <br />
Chinmay Raghvendran (**cr64**) <br />
Lucas Sanson (**lsanson2**) <br />

## 1. Project Documentation (README)

### Features
- **Intelligent Input Handling**: Accepts exact IMDb Film IDs (e.g., `tt0133093`) or movie titles via interactive fuzzy search.
- **Dual-Extraction Engine**:
  - **Part 1 (Cinemagoer)**: High-fidelity scraper using the `cinemagoer` library with advanced WAF-bypass techniques (User-Agent spoofing and connection throttling).
  - **Part 2 (Official Datasets)**: Robust fallback engine that processes millions of rows from compressed IMDb `.tsv.gz` files using memory-safe `pandas` chunking.
- **Data Enrichment**: Calculates current ages from birth years and cleanses JSON character data into a readable format.
- **Structured Export**: Generates standardized CSV reports containing IMDb IDs, Name, Role Category, Character, Age, and Gender.

### Requirements
- Python 3.11+
- Libraries: `pandas`, `cinemagoer`, `requests`

### Installation
```bash
# Clone the repository
git clone [https://github.com/Lsanson1987/Cinema-Scraper.git](https://github.com/Lsanson1987/Cinema-Scraper.git)
cd Cinema-Scraper

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pandas cinemagoer requests
