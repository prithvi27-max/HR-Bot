# ============================================
# 📊 visualizer.py
# ============================================
import plotly.express as px

def plot_headcount_trend(df):
    return px.line(df, x="Year", y="Active_Headcount", title="Active Headcount Trend", markers=True)

def plot_attrition(df):
    return px.bar(df, x="Year", y="Attrition_Rate(%)", title="Yearly Attrition Rate (%)")

def plot_salary_trend(df):
    return px.line(df, x="Year", y="Avg_Salary", title="Average Salary Trend", markers=True)

def plot_engagement(df):
    return px.bar(df, x="Department", y="mean", title="Engagement Score by Department")

def plot_diversity(df):
    return px.bar(df, x="Department", y="Count", color="Gender", barmode="group", title="Gender Diversity by Department")
