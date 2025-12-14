import pandas as pd
from pathlib import Path
import re

RAW_DIR = Path("../data/raw")
PROC_DIR = Path("../data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

def extract_year_from_filename(fname):
    match = re.search(r"(20\d{2})", fname)
    return int(match.group(1)) if match else None

def load_raw_files():
    files = list(RAW_DIR.glob("*.csv"))
    loaded = []

    for f in files:
        try:
            df = pd.read_csv(f, dtype=str)
            loaded.append((f.name, df))
            print(f"[loaded] {f.name}")
        except Exception as e:
            print(f"[failed] {f.name}: {e}")
    return loaded

def clean_column_names(df):
    df = df.copy()
    df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(r"[^a-z0-9_]", "", regex=True))
    return df

def unify_value_column(df):
    df = df.copy()
    cols = df.columns

    if "diabetes_adjprev" in cols:
        df["value"] = pd.to_numeric(df["diabetes_adjprev"], errors="coerce")
        return df

    if "diabetes_crudeprev" in cols:
        df["value"] = pd.to_numeric(df["diabetes_crudeprev"], errors="coerce")
        return df

    candidate_keywords = ["prevalence", "percent", "percentage", "value", "rate", "incidence"]
    candidates = [c for c in cols if any(k in c for k in candidate_keywords)]

    if candidates:
        col = candidates[0]
        df.rename(columns={col: "value"}, inplace=True)
        df["value"] = pd.to_numeric(df["value"].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False),errors="coerce")
        return df

    print(f"[warning] Nothing detected in columns: {list(cols)}")
    df["value"] = pd.NA
    return df

def detect_level_from_filename(fname):
    fname = fname.lower()
    if "county" in fname:
        return "county"
    if "state" in fname:
        return "state"
    return "unknown"

def detect_type_from_filename(fname):
    fname = fname.lower()
    if "prevalence" in fname:
        return "prevalence"
    if "incidence" in fname:
        return "incidence"
    return "unknown"


def extract_year_from_df(df):
    year_cols = [c for c in df.columns if "year" in c]

    if not year_cols:
        return None

    col = year_cols[0]
    years = df[col].dropna().unique()
    years = [y for y in years if re.match(r"^20\d{2}$", str(y))]

    if len(years) == 1:
        return int(years[0])
    return None

def merge_datasets():
    loaded = load_raw_files()
    prevalence_state = []
    prevalence_county = []
    incidence_state = []

    for fname, df in loaded:
        df = clean_column_names(df)
        df = unify_value_column(df)
        level = detect_level_from_filename(fname)
        dtype = detect_type_from_filename(fname)
        year = extract_year_from_filename(fname)

        if year is None:
            y2 = extract_year_from_df(df)
            year = y2 if y2 is not None else 0

        df["year"] = year

        if dtype == "prevalence":
            if level == "state":
                prevalence_state.append(df)
            elif level == "county":
                prevalence_county.append(df)
        elif dtype == "incidence":
            if level == "state":
                incidence_state.append(df)

    if prevalence_state:
        out = pd.concat(prevalence_state, ignore_index=True)
        out.to_csv(PROC_DIR / "prevalence_state_clean.csv", index=False)
        print("[saved] prevalence_state_clean.csv")

    if prevalence_county:
        out = pd.concat(prevalence_county, ignore_index=True)
        out.to_csv(PROC_DIR / "prevalence_county_clean.csv", index=False)
        print("[saved] prevalence_county_clean.csv")

    if incidence_state:
        out = pd.concat(incidence_state, ignore_index=True)
        out.to_csv(PROC_DIR / "incidence_state_clean.csv", index=False)
        print("[saved] incidence_state_clean.csv")

merge_datasets()