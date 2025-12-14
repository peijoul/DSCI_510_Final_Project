import pandas as pd
import numpy as np
from pathlib import Path

df_state = pd.read_csv("../data/processed/prevalence_state_clean.csv")
df_county = pd.read_csv("../data/processed/prevalence_county_clean.csv")

measures_to_analyze = ["Diabetes"]
df_state = df_state[df_state['short_question_text'].isin(measures_to_analyze)]
df_county = df_county[df_county['short_question_text'].isin(measures_to_analyze)]
df_state['stateabbr'] = df_state['stateabbr'].astype(str).str.strip()
df_county['locationname'] = df_county['locationname'].astype(str).str.strip()

RESULTS_DIR = Path("../results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def descriptive_stats(df, level, filename):
    stats = df.groupby('short_question_text')['data_value'].agg(['count', 'mean', 'std', 'min', 'max'])
    stats.to_excel(RESULTS_DIR / filename)
    print(f"[Saved] {filename}")

def yearly_trend(df, level, filename):
    with pd.ExcelWriter(RESULTS_DIR / filename) as writer:
        for measure in measures_to_analyze:
            df_measure = df[df['short_question_text'] == measure]
            trend = df_measure.groupby('year')['data_value'].agg(['count', 'mean', 'std', 'min', 'max'])
            trend.to_excel(writer, sheet_name=measure)
    print(f"[Saved] {filename}")

def compare_location(df, level, filename):
    location_col = 'stateabbr' if level == 'State' else 'locationname'
    with pd.ExcelWriter(RESULTS_DIR / filename) as writer:
        for measure in measures_to_analyze:
            df_measure = df[df['short_question_text'] == measure]
            comp = df_measure.groupby(location_col)['data_value'].agg(['count', 'mean', 'std', 'min', 'max']).sort_values('mean', ascending=False)
            comp.to_excel(writer, sheet_name=measure)
    print(f"[Saved] {filename}")

descriptive_stats(df_state, "State-level", "state_descriptive.xlsx")
descriptive_stats(df_county, "County-level", "county_descriptive.xlsx")
yearly_trend(df_state, "State-level", "state_yearly_trend.xlsx")
yearly_trend(df_county, "County-level", "county_yearly_trend.xlsx")
compare_location(df_state, "State", "state_location_comparison.xlsx")
compare_location(df_county, "County", "county_location_comparison.xlsx")

state_trend_csv = df_state.groupby(['year', 'short_question_text'])['data_value'] \
    .mean().reset_index()
state_trend_csv.to_csv(RESULTS_DIR / "state_yearly_trend.csv", index=False)
county_trend_csv = df_county.groupby(['year', 'short_question_text'])['data_value'] \
    .mean().reset_index()
county_trend_csv.to_csv(RESULTS_DIR / "county_yearly_trend.csv", index=False)
print("[Saved] state_yearly_trend.csv")
print("[Saved] county_yearly_trend.csv")

state_compare_csv = df_state.groupby(['stateabbr', 'short_question_text'])['data_value'] \
    .mean().reset_index()
state_compare_csv.to_csv(RESULTS_DIR / "state_location_comparison.csv", index=False)
county_compare_csv = df_county.groupby(['locationname', 'short_question_text'])['data_value'] \
    .mean().reset_index()
county_compare_csv.to_csv(RESULTS_DIR / "county_location_comparison.csv", index=False)
print("[Saved] state_location_comparison.csv")
print("[Saved] county_location_comparison.csv")