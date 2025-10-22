# ============================================
# 📘 data_utils.py
# ============================================
import pandas as pd
import numpy as np

# --------------------------------------------
# Load and Prepare Data
# --------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    """
    Load and preprocess the HR dataset.
    """
    df = pd.read_csv(path, parse_dates=["Hire_Date", "Termination_Date"])
    df["Year_Hired"] = df["Hire_Date"].dt.year
    df["Year_Terminated"] = df["Termination_Date"].dt.year
    df["Active_Flag"] = np.where(df["Status"] == "Active", 1, 0)
    return df


# --------------------------------------------
# HR Metrics
# --------------------------------------------
def headcount_trend(df: pd.DataFrame):
    """
    Calculate active headcount per year.
    """
    years = range(df["Hire_Date"].dt.year.min(), df["Hire_Date"].dt.year.max() + 1)
    trend = []
    for y in years:
        active = df[(df["Hire_Date"].dt.year <= y) &
                    ((df["Termination_Date"].isna()) | (df["Termination_Date"].dt.year > y))]
        trend.append({"Year": y, "Active_Headcount": len(active)})
    return pd.DataFrame(trend)


def attrition_rate(df: pd.DataFrame):
    """
    Compute yearly attrition rate (%).
    """
    yearly = df.groupby("Year_Terminated").size().reset_index(name="Attritions")
    hires = df.groupby("Year_Hired").size().reset_index(name="Hires")

    combined = pd.merge(hires, yearly, left_on="Year_Hired", right_on="Year_Terminated", how="outer").fillna(0)
    combined["Year"] = combined["Year_Hired"].fillna(combined["Year_Terminated"])
    combined = combined.sort_values("Year")
    combined["Attrition_Rate(%)"] = (combined["Attritions"] / (combined["Hires"] + 1e-5)) * 100
    return combined[["Year", "Hires", "Attritions", "Attrition_Rate(%)"]]


def avg_salary_trend(df: pd.DataFrame):
    """
    Average salary per year.
    """
    df["Year"] = df["Hire_Date"].dt.year
    return df.groupby("Year")["Salary"].mean().reset_index(name="Avg_Salary")


def engagement_summary(df: pd.DataFrame):
    """
    Engagement score summary by department.
    """
    return df.groupby("Department")["Engagement_Score"].agg(["mean", "min", "max", "count"]).reset_index()


def gender_diversity(df: pd.DataFrame):
    """
    Gender distribution across departments.
    """
    return df.groupby(["Department", "Gender"]).size().reset_index(name="Count")


# --------------------------------------------
# Helper
# --------------------------------------------
def available_metrics():
    """
    Return available HR analytics functions for reference.
    """
    return {
        "headcount": "Active headcount trend per year",
        "attrition": "Yearly attrition rate",
        "salary": "Average salary trend",
        "engagement": "Engagement score summary by department",
        "diversity": "Gender diversity by department"
    }
