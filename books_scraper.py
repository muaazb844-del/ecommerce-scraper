"""
============================================================
  E-commerce Product Data Scraper
  Target : books.toscrape.com
  Tools  : Python, BeautifulSoup, Pandas
  Output : books_data.csv
============================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# ── Configuration ────────────────────────────────────────
BASE_URL   = "https://books.toscrape.com/catalogue/"
START_URL  = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT_CSV = "books_data.csv"
DELAY      = 1.0          # seconds between requests (be polite!)
MAX_PAGES  = None         # set to an integer to limit pages, e.g. 5

# Word-to-number map for star ratings
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3,
    "Four": 4, "Five": 5
}


# ── Helpers ──────────────────────────────────────────────
def get_soup(url: str) -> BeautifulSoup | None:
    """Fetch a page and return a BeautifulSoup object, or None on failure."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (educational scraper)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def parse_books(soup: BeautifulSoup) -> list[dict]:
    """Extract all book records from a single catalogue page."""
    books = []
    articles = soup.select("article.product_pod")

    for article in articles:
        # Title
        title = article.select_one("h3 a")["title"]

        # Price – strip the £ symbol and convert to float
        price_text = article.select_one("p.price_color").text.strip()
        price = float(price_text.replace("£", "").replace("Â", "").strip())

        # Star rating – stored as a CSS class word e.g. "Three"
        rating_word = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_word, 0)

        # Availability
        availability = article.select_one("p.availability").text.strip()

        books.append({
            "Title"       : title,
            "Price (£)"   : price,
            "Star Rating" : rating,
            "Availability": availability,
        })

    return books


def get_next_page(soup: BeautifulSoup) -> str | None:
    """Return the absolute URL of the next page, or None if on the last page."""
    next_btn = soup.select_one("li.next a")
    if next_btn:
        return BASE_URL + next_btn["href"]
    return None


# ── Main scraper loop ────────────────────────────────────
def scrape(start_url: str = START_URL, max_pages: int | None = MAX_PAGES) -> pd.DataFrame:
    all_books = []
    url       = start_url
    page_num  = 0

    print("=" * 55)
    print("  Books.toscrape.com — Product Data Scraper")
    print("=" * 55)

    while url:
        page_num += 1
        if max_pages and page_num > max_pages:
            print(f"\n  Reached page limit ({max_pages}). Stopping.")
            break

        print(f"  Scraping page {page_num:>3} → {url}")
        soup = get_soup(url)

        if soup is None:
            print("  Skipping page due to fetch error.")
            url = None
            break

        books = parse_books(soup)
        all_books.extend(books)
        print(f"             ✔  {len(books)} books collected "
              f"(total so far: {len(all_books)})")

        url = get_next_page(soup)
        if url:
            time.sleep(DELAY)   # be a polite scraper

    print("\n" + "=" * 55)
    print(f"  Scraping complete. Total books: {len(all_books)}")
    print("=" * 55)

    return pd.DataFrame(all_books)


# ── Data cleaning ────────────────────────────────────────
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning steps to the raw scraped DataFrame."""
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["Title"])
    dupes = before - len(df)
    if dupes:
        print(f"  [CLEAN] Removed {dupes} duplicate row(s).")

    # Ensure correct dtypes
    df["Price (£)"]   = pd.to_numeric(df["Price (£)"], errors="coerce")
    df["Star Rating"] = pd.to_numeric(df["Star Rating"], errors="coerce").astype("Int64")

    # Strip whitespace from string columns
    for col in ["Title", "Availability"]:
        df[col] = df[col].str.strip()

    # Sort by rating desc, then price asc
    df = df.sort_values(["Star Rating", "Price (£)"],
                        ascending=[False, True]).reset_index(drop=True)

    print(f"  [CLEAN] Dataset ready: {len(df)} rows × {len(df.columns)} columns.")
    return df


# ── Summary report ───────────────────────────────────────
def print_summary(df: pd.DataFrame) -> None:
    print("\n── Quick Summary ──────────────────────────────────")
    print(f"  Total books      : {len(df)}")
    print(f"  Avg price        : £{df['Price (£)'].mean():.2f}")
    print(f"  Cheapest book    : £{df['Price (£)'].min():.2f}")
    print(f"  Most expensive   : £{df['Price (£)'].max():.2f}")
    print(f"  5-star books     : {(df['Star Rating'] == 5).sum()}")
    print(f"  In stock         : {df['Availability'].str.contains('In stock').sum()}")
    print("\n── Top 5 Cheapest 5-Star Books ────────────────────")
    top5 = (df[df["Star Rating"] == 5]
            .nsmallest(5, "Price (£)")[["Title", "Price (£)"]])
    print(top5.to_string(index=False))
    print("─" * 51)


# ── Entry point ──────────────────────────────────────────
if __name__ == "__main__":
    # Allow an optional CLI argument to limit pages, e.g.: python books_scraper.py 3
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_PAGES

    raw_df   = scrape(max_pages=limit)
    clean_df = clean(raw_df)

    clean_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\n  ✅  Data saved to '{OUTPUT_CSV}'")

    print_summary(clean_df)
