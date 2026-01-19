import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

RAW_DATA_PATH = "data/raw/cardio_train.csv"
PROCESSED_DATA_PATH = "data/processed/cardio_clean.csv"

TABLES_DIR = "reports/tables"
FIGURES_DIR = "reports/figures"


def create_directories() -> None:
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    # cardio_train.csv typically uses ';' as separator
    return pd.read_csv(path, sep=";")


def audit_data(df: pd.DataFrame) -> pd.DataFrame:
    audit = {
        "rows": len(df),
        "columns": df.shape[1],
        "duplicates": int(df.duplicated().sum()),
        "max_missing_ratio": float(df.isna().mean().max())
    }
    return pd.DataFrame([audit])


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1) Remove full duplicates
    df = df.drop_duplicates()

    # 2) Convert age days -> years
    df["age_years"] = (df["age"] / 365.25).round(1)

    # 3) Ensure numeric types for key measurements
    for col in ["height", "weight", "ap_hi", "ap_lo"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4) Apply physiologically reasonable ranges
    df.loc[~df["height"].between(120, 220), "height"] = np.nan
    df.loc[~df["weight"].between(35, 200), "weight"] = np.nan
    df.loc[~df["ap_hi"].between(70, 250), "ap_hi"] = np.nan
    df.loc[~df["ap_lo"].between(40, 150), "ap_lo"] = np.nan

    # 5) Logical constraint: systolic must be greater than diastolic
    bad_bp = df["ap_hi"].notna() & df["ap_lo"].notna() & (df["ap_hi"] <= df["ap_lo"])
    df.loc[bad_bp, ["ap_hi", "ap_lo"]] = np.nan

    # 6) Fill remaining NaNs with median (simple, robust method)
    for col in ["height", "weight", "ap_hi", "ap_lo"]:
        df[col] = df[col].fillna(df[col].median())

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # BMI
    height_m = df["height"] / 100.0
    df["bmi"] = (df["weight"] / (height_m ** 2)).round(2)

    # Pulse pressure
    df["pulse_pressure"] = df["ap_hi"] - df["ap_lo"]

    # Risk flags (simple thresholds)
    df["hypertension"] = ((df["ap_hi"] >= 140) | (df["ap_lo"] >= 90)).astype(int)
    df["obesity"] = (df["bmi"] >= 30).astype(int)

    return df


def save_tables(df: pd.DataFrame) -> None:
    # Descriptive stats
    df.describe().round(2).to_csv(os.path.join(TABLES_DIR, "descriptive_statistics.csv"))

    # Group comparison by target (cardio 0/1)
    cols = ["age_years", "ap_hi", "ap_lo", "bmi", "pulse_pressure"]
    group_stats = (
        df.groupby("cardio")[cols]
        .agg(["mean", "median", "std"])
        .round(2)
    )
    group_stats.to_csv(os.path.join(TABLES_DIR, "group_comparison.csv"))

    # Correlations (numeric only)
    corr = df[cols + ["cholesterol", "gluc", "smoke", "alco", "active", "cardio"]].corr(numeric_only=True)
    corr.to_csv(os.path.join(TABLES_DIR, "correlation_matrix.csv"))


def save_figures(df: pd.DataFrame) -> None:
    # BMI histogram
    plt.figure()
    plt.hist(df["bmi"].dropna(), bins=40)
    plt.title("BMI distribution")
    plt.xlabel("BMI")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "bmi_distribution.png"), dpi=200)
    plt.close()

    # Systolic BP boxplot by cardio
    plt.figure()
    df.boxplot(column="ap_hi", by="cardio")
    plt.title("Systolic blood pressure by cardio group")
    plt.suptitle("")
    plt.xlabel("Cardio (0=no, 1=yes)")
    plt.ylabel("ap_hi")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ap_hi_boxplot_by_cardio.png"), dpi=200)
    plt.close()


def main() -> None:
    create_directories()

    df_raw = load_data(RAW_DATA_PATH)

    audit = audit_data(df_raw)
    audit.to_csv(os.path.join(TABLES_DIR, "audit_summary.csv"), index=False)

    df_clean = clean_data(df_raw)
    df_final = add_features(df_clean)

    save_tables(df_final)
    save_figures(df_final)

    df_final.to_csv(PROCESSED_DATA_PATH, index=False)
    print("DONE. Output saved to data/processed and reports/.")


if __name__ == "__main__":
    main()
