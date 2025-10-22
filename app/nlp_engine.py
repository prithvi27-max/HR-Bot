# ============================================
# 🧠 nlp_engine.py — Final Version (Rule-based + HR Question Bank)
# ============================================
import re

def get_intent(query: str):
    """
    Detect HR metric intent and extract filters (like department, year).
    Uses rule-based logic + predefined HR question patterns.
    """
    query = query.lower().strip()
    intent = None
    filters = {}

    # --------------------------------------------
    # 🎯 HR Question Bank (known phrases)
    # --------------------------------------------
    question_bank = {
        # Headcount trends
        "headcount trend": "headcount",
        "active employees": "headcount",
        "employee count": "headcount",
        "total employees": "headcount",
        "employees over years": "headcount",

        # Gender
        "headcount by gender": "headcount_gender",
        "gender ratio": "headcount_gender",
        "male female": "headcount_gender",
        "gender split": "headcount_gender",

        # Department
        "headcount by department": "headcount_department",
        "employees by department": "headcount_department",
        "department headcount": "headcount_department",

        # Attrition
        "attrition rate": "attrition",
        "resignation trend": "attrition",
        "turnover": "attrition",
        "employee exits": "attrition",

        # Salary
        "average salary": "salary",
        "salary trend": "salary",
        "pay trend": "salary",
        "compensation trend": "salary",

        # Engagement
        "engagement score": "engagement",
        "employee satisfaction": "engagement",
        "employee happiness": "engagement",

        # Diversity
        "diversity": "diversity",
        "gender diversity": "diversity"
    }

    # --------------------------------------------
    # 🔍 Match known question patterns
    # --------------------------------------------
    for key, val in question_bank.items():
        if key in query:
            intent = val
            break

    # --------------------------------------------
    # 🧩 Backup keyword-based logic (for unseen phrasings)
    # --------------------------------------------
    if not intent:
        if any(word in query for word in ["headcount", "employees", "strength"]):
            if "gender" in query or "male" in query or "female" in query:
                intent = "headcount_gender"
            elif "department" in query or "function" in query:
                intent = "headcount_department"
            else:
                intent = "headcount"
        elif any(word in query for word in ["attrition", "resignation", "turnover"]):
            intent = "attrition"
        elif any(word in query for word in ["salary", "pay", "compensation"]):
            intent = "salary"
        elif any(word in query for word in ["engagement", "satisfaction", "happiness"]):
            intent = "engagement"
        elif any(word in query for word in ["diversity", "ratio"]):
            intent = "diversity"

    # --------------------------------------------
    # 🧾 Extract filters
    # --------------------------------------------
    # Department filter
    dept_match = re.search(r"(it|finance|hr|marketing|operations|sales|r&d)", query)
    if dept_match:
        filters["department"] = dept_match.group(1).capitalize()

    # Year filters
    year_match = re.findall(r"(20\d{2})", query)
    if year_match:
        filters["year"] = list(map(int, year_match))

    return intent, filters
