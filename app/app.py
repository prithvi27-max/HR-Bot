# ============================================
# 💬 app.py — ChatGPT-Style Conversational HR Assistant (Persistent Visuals)
# ============================================
import streamlit as st
from data_utils import (
    load_data, headcount_trend, attrition_rate,
    avg_salary_trend, engagement_summary, gender_diversity
)
from nlp_engine import get_intent
import plotly.express as px
import pandas as pd

# --------------------------------------------
# 🎨 Page Configuration
# --------------------------------------------
st.set_page_config(page_title="HR Analytics Assistant", layout="wide")
# Display a logo or title image
st.image("assets/Image.png", width=100)  # Path to your JPG image
st.title("HR Analytics Assistant")
st.caption("Ask about your HR data — headcount, attrition, salary, engagement, diversity, etc.")

# --------------------------------------------
# 🧠 Session State (Chat Memory)
# --------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store (role, content, chart_data)

# --------------------------------------------
# Load Dataset Once
# --------------------------------------------
df = load_data("data/hr_master_10000.csv")

# --------------------------------------------
# Helper HR Metric Functions
# --------------------------------------------
def headcount_by_gender(df):
    active = df[df["Status"] == "Active"]
    return active.groupby("Gender").size().reset_index(name="Headcount")

def headcount_by_department(df):
    active = df[df["Status"] == "Active"]
    return active.groupby("Department").size().reset_index(name="Headcount")

# --------------------------------------------
# Function to Process Query
# --------------------------------------------
def process_query(query: str):
    intent, filters = get_intent(query)
    df_filtered = df.copy()

    # Apply department filter if found
    if "department" in filters:
        df_filtered = df_filtered[df_filtered["Department"].str.lower() == filters["department"].lower()]

    chart = None
    result = None
    response_text = ""

    if intent == "headcount":
        result = headcount_trend(df_filtered)
        chart = px.line(result, x="Year", y="Active_Headcount", text="Active_Headcount", markers=True,
                        title="📈 Active Headcount Trend")
        chart.update_traces(textposition="top center")
        response_text = "Here’s the headcount trend over the years."

    elif intent == "headcount_gender":
        result = headcount_by_gender(df_filtered)
        chart = px.bar(result, x="Gender", y="Headcount", text="Headcount", title="👩‍💼 Headcount by Gender")
        chart.update_traces(textposition="outside")
        response_text = "Here’s the active headcount split by gender."

    elif intent == "headcount_department":
        result = headcount_by_department(df_filtered)
        chart = px.bar(result, x="Department", y="Headcount", text="Headcount", title="🏢 Headcount by Department")
        chart.update_traces(textposition="outside")
        response_text = "Here’s the current headcount across departments."

    elif intent == "attrition":
        result = attrition_rate(df_filtered)
        chart = px.bar(result, x="Year", y="Attrition_Rate(%)", text="Attrition_Rate(%)", title="📉 Attrition Rate by Year")
        chart.update_traces(textposition="outside")
        response_text = "Here’s the attrition trend by year."

    elif intent == "salary":
        result = avg_salary_trend(df_filtered)
        chart = px.line(result, x="Year", y="Avg_Salary", text="Avg_Salary", markers=True,
                        title="💰 Average Salary Trend")
        chart.update_traces(textposition="top center")
        response_text = "Here’s the salary trend you requested."

    elif intent == "engagement":
        result = engagement_summary(df_filtered)
        chart = px.bar(result, x="Department", y="mean", text="mean", title="💬 Engagement by Department")
        chart.update_traces(textposition="outside")
        response_text = "Here’s how engagement scores look by department."

    elif intent == "diversity":
        result = gender_diversity(df_filtered)
        chart = px.bar(result, x="Department", y="Count", color="Gender", text="Count",
                       barmode="group", title="🌍 Gender Diversity by Department")
        chart.update_traces(textposition="outside")
        response_text = "Here’s the gender diversity overview."

    else:
        response_text = "Sorry, I couldn’t understand that query yet. Try asking about headcount, salary, or attrition."

    return response_text, chart, result

# --------------------------------------------
# Render Chat History
# --------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("chart") is not None:
            st.plotly_chart(msg["chart"], use_container_width=True)
        if msg.get("data") is not None:
            st.dataframe(msg["data"])

# --------------------------------------------
# Chat Input (New Message)
# --------------------------------------------
query = st.chat_input("Ask your HR query...")

if query:
    # Display User Message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Process Response
    response_text, chart, data = process_query(query)

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.markdown(response_text)
        if chart is not None:
            st.plotly_chart(chart, use_container_width=True)
        if data is not None:
            st.dataframe(data)

    # Save to Session (for persistence)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "chart": chart,
        "data": data
    })
