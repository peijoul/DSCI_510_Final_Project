import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("../results")
state_trend = pd.read_csv(RESULTS_DIR / "state_yearly_trend.csv")
county_trend = pd.read_csv(RESULTS_DIR / "county_yearly_trend.csv")
state_compare = pd.read_csv(RESULTS_DIR / "state_location_comparison.csv")
county_compare = pd.read_csv(RESULTS_DIR / "county_location_comparison.csv")
measures = ["Diabetes"]

def plot_state_trend(measure):
    df_plot = state_trend[state_trend["short_question_text"] == measure]
    plt.figure(figsize=(10, 5))

    if df_plot.shape[0] >= 2:
        plt.plot(df_plot["year"], df_plot["data_value"], marker="o")
        plt.title(f"State-Level Trend: {measure}", fontsize=14)
    else:
        single_row = df_plot.iloc[0]
        plt.scatter([single_row["year"]], [single_row["data_value"]], s=120)
        plt.title(f"State-Level Trend: {measure} (Only 1 Year Available)", fontsize=14)
        plt.annotate(
            f"{int(single_row['year'])}: {single_row['data_value']:.2f}",
            (single_row["year"], single_row["data_value"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=10
        )

    plt.xlabel("Year")
    plt.ylabel("Average Prevalence (%)")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / f"state_trend_{measure}.png", dpi=300)
    plt.show()
    plt.close()

def plot_state_top20(measure):
    df_plot = (state_compare[state_compare["short_question_text"] == measure].sort_values("data_value", ascending=False).head(20))

    if df_plot.empty:
        print(f"[Skip] No state comparison data for {measure}")
        return

    plt.figure(figsize=(10, 8))
    colors = plt.cm.tab20(np.arange(len(df_plot)))
    bars = plt.barh(df_plot["stateabbr"], df_plot["data_value"], color=colors)

    for bar in bars:
        width = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        plt.text(width + 0.3, y, f"{width:.1f}", va="center", fontsize=9)

    plt.title(f"Top 20 States: {measure}", fontsize=14)
    plt.xlabel("Average Prevalence (%)")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"state_top20_{measure}.png", dpi=300)
    plt.show()
    plt.close()

def plot_county_trend(measure):
    df_plot = county_trend[county_trend["short_question_text"] == measure]
    if df_plot.empty:
        print(f"[Skip] No county-level data found for {measure}")
        return

    plt.figure(figsize=(10, 5))
    if df_plot.shape[0] >= 2:
        plt.plot(df_plot["year"], df_plot["data_value"], marker="o")
        plt.title(f"County-Level Trend: {measure}", fontsize=14)
    else:
        single_row = df_plot.iloc[0]
        plt.scatter(single_row["year"], single_row["data_value"], s=140)
        plt.title(f"County-Level Trend: {measure} (Only 1 Year Available)", fontsize=14)
        plt.annotate(
            f"{single_row['year']}: {single_row['data_value']:.2f}",
            (single_row["year"], single_row["data_value"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=10
        )

    plt.xlabel("Year")
    plt.ylabel("Average Prevalence (%)")
    plt.grid(True)
    plt.savefig(RESULTS_DIR / f"county_trend_{measure}.png", dpi=300)
    plt.show()
    plt.close()

def plot_county_top20(measure):
    df_plot = (county_compare[county_compare["short_question_text"] == measure].sort_values("data_value", ascending=False).head(20))
    if df_plot.empty:
        print(f"[Skip] No county comparison data for {measure}")
        return

    plt.figure(figsize=(12, 10))
    colors = plt.cm.tab20(np.arange(len(df_plot)))
    bars = plt.barh(df_plot["locationname"], df_plot["data_value"], color=colors)
    for bar in bars:
        width = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        plt.text(width + 0.3, y, f"{width:.1f}", va="center", fontsize=8)

    plt.title(f"Top 20 Counties: {measure}", fontsize=14)
    plt.xlabel("Average Prevalence (%)")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"county_top20_{measure}.png", dpi=300)
    plt.show()
    plt.close()

for measure in measures:
    print(f"[Info] Plotting State Trend: {measure}")
    plot_state_trend(measure)

    print(f"[Info] Plotting State Top 20: {measure}")
    plot_state_top20(measure)

    print(f"[Info] Plotting County Trend: {measure}")
    plot_county_trend(measure)

    print(f"[Info] Plotting County Top 20: {measure}")
    plot_county_top20(measure)