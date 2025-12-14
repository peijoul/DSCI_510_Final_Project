import time
import requests
from pathlib import Path
import pandas as pd
import io
from bs4 import BeautifulSoup

RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {"prevalence_county": "duw2-7jbt", "prevalence_state": "6vp6-wxuq", "incidence_state": "i46a-9kgh"}

YEARS = list(range(2004, 2024))
REQUEST_TIMEOUT = 30
SLEEP_BETWEEN = 0.2

def download_csv(dataset_id):
    url = f"https://data.cdc.gov/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"
    print(f"[Downloading] {url}")

    r = requests.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.content

def save_rows_by_year(csv_bytes, dataset_key, dataset_id, year):
    df = pd.read_csv(io.BytesIO(csv_bytes), dtype=str)
    year_cols = [c for c in df.columns if "year" in c.lower()]

    if not year_cols:
        out = RAW_DIR / f"{dataset_key}_{dataset_id}_all.csv"
        if out.exists():
            print(f"[skip] {out}")
        else:
            df.to_csv(out, index=False)
            print(f"[saved] {out}")
        return

    ycol = year_cols[0]
    df_year = df[df[ycol].astype(str).str.contains(str(year), na=False)]

    if df_year.empty:
        print(f"[no data] {dataset_key} {year}")
        return

    out = RAW_DIR / f"{dataset_key}_{dataset_id}_{year}.csv"
    df_year.to_csv(out, index=False)
    print(f"[saved] {out}")

def scrape_cdc_html(url):
    print(f"[Scraping HTML] {url}")

    r = requests.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    parts = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        parts.append(tag.get_text(strip=True))

    for tag in soup.find_all("p"):
        parts.append(tag.get_text(strip=True))

    for tag in soup.find_all("li"):
        parts.append("- " + tag.get_text(strip=True))

    final_text = "\n".join(parts)

    out = RAW_DIR / "cdc_diabetes_info.txt"
    out.write_text(final_text, encoding="utf-8")

    print(f"[saved HTML text] {out}")

for key, dsid in DATASETS.items():
    try:
        csv_bytes = download_csv(dsid)
    except Exception as e:
        print(f"[fail] {dsid}: {e}")
        continue

    for yr in YEARS:
        try:
            save_rows_by_year(csv_bytes, key, dsid, yr)
        except Exception as e:
            print(f"[fail year {yr}] {e}")

        time.sleep(SLEEP_BETWEEN)

url = "https://www.cdc.gov/diabetes/php/data-research/data-statistics/index.html"
scrape_cdc_html(url)