"""
AEWIS - Academic Early Warning & Intervention System
=====================================================
Frontend-only implementation using Streamlit + Plotly + Pandas
All backend integration points are clearly marked with # BACKEND INTEGRATION POINT

Architecture:
  - UI Layer:        render_* functions
  - Data Layer:      mock_* functions (demo data)
  - API Layer:       fetch_* / assign_* functions (placeholder stubs)
"""

import streamlit as st
from backend_connector import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  CONFIGURATION & THEME
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AEWIS | Academic Early Warning System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Color palette
C_RED    = "#DC2626"
C_YELLOW = "#F59E0B"
C_GREEN  = "#10B981"
C_BLUE   = "#3B82F6"
C_DARK   = "#0F172A"
C_CARD   = "#1E293B"
C_TEXT   = "#F1F5F9"

GLOBAL_CSS = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
    background-color: {C_DARK};
    color: {C_TEXT};
  }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
    background: #0B1120;
    border-right: 1px solid #1E293B;
  }}
  section[data-testid="stSidebar"] * {{ color: {C_TEXT} !important; }}

  /* Cards */
  .kpi-card {{
    background: {C_CARD};
    border-radius: 12px;
    padding: 20px 24px;
    border: 1px solid #2D3748;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
  }}
  .kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 12px 0 0 12px;
  }}
  .kpi-card.red::before   {{ background: {C_RED}; }}
  .kpi-card.yellow::before {{ background: {C_YELLOW}; }}
  .kpi-card.green::before  {{ background: {C_GREEN}; }}
  .kpi-card.blue::before   {{ background: {C_BLUE}; }}

  .kpi-value {{
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
  }}
  .kpi-label {{
    font-size: 0.8rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
  }}
  .kpi-delta {{
    font-size: 0.85rem;
    margin-top: 8px;
  }}

  /* Risk badges */
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
  }}
  .badge-high   {{ background: rgba(220,38,38,0.2);  color: {C_RED}; }}
  .badge-medium {{ background: rgba(245,158,11,0.2); color: {C_YELLOW}; }}
  .badge-low    {{ background: rgba(16,185,129,0.2); color: {C_GREEN}; }}

  /* Section headers */
  .section-header {{
    font-size: 1.5rem;
    font-weight: 700;
    color: {C_TEXT};
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .section-sub {{
    font-size: 0.9rem;
    color: #64748B;
    margin-bottom: 24px;
  }}

  /* Chat bubbles */
  .chat-user {{
    background: {C_BLUE};
    color: white;
    border-radius: 16px 16px 4px 16px;
    padding: 10px 16px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    font-size: 0.9rem;
  }}
  .chat-bot {{
    background: {C_CARD};
    border: 1px solid #2D3748;
    border-radius: 16px 16px 16px 4px;
    padding: 10px 16px;
    margin: 8px 0;
    max-width: 75%;
    font-size: 0.9rem;
  }}
  .robot-icon {{
    font-size: 2rem;
    margin-bottom: 4px;
  }}

  /* XP bar */
  .xp-bar-bg {{
    background: #1E293B;
    border-radius: 6px;
    height: 10px;
    margin-top: 6px;
    overflow: hidden;
  }}
  .xp-bar-fill {{
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
  }}

  /* Student cards */
  .student-card {{
    background: {C_CARD};
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #2D3748;
    margin-bottom: 12px;
    transition: border-color 0.2s;
  }}
  .student-card:hover {{ border-color: {C_BLUE}; }}

  /* Page title */
  .page-title {{
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, {C_BLUE}, {C_GREEN});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
  }}

  /* Hide default streamlit elements */
  #MainMenu {{ visibility: hidden; }}
  footer    {{ visibility: hidden; }}
  header    {{ visibility: hidden; }}

  /* Plotly charts background */
  .js-plotly-plot .plotly {{ background: transparent !important; }}

  /* Dividers */
  hr {{ border-color: #1E293B; margin: 24px 0; }}

  /* Tables */
  .dataframe {{
    background: {C_CARD} !important;
    color: {C_TEXT} !important;
    font-size: 0.85rem !important;
  }}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  MOCK DATA LAYER  (all demo data lives here)
# ═══════════════════════════════════════════════════════════

DEPARTMENTS   = ["Computer Science", "Mathematics", "Physics", "Business", "Arts", "Biology"]
MENTORS       = ["Dr. Sharma", "Prof. Lee", "Dr. Patel", "Ms. Johnson", "Mr. Gupta", "Dr. Kim"]
RISK_LEVELS   = ["High", "Medium", "Low"]
RISK_COLORS   = {"High": C_RED, "Medium": C_YELLOW, "Low": C_GREEN}

@st.cache_data
def mock_students(n=120):
    np.random.seed(42)
    names_first = ["Aarav","Priya","James","Sofia","Liam","Aria","Noah","Mia","Ethan","Emma",
                   "Oliver","Amelia","Aiden","Luna","Lucas","Chloe","Mason","Layla","Logan","Ella"]
    names_last  = ["Kumar","Singh","Smith","Patel","Johnson","Lee","Brown","Davis","Wilson","Moore"]
    students = []
    for i in range(n):
        risk_w = np.random.choice(["High","Medium","Low"], p=[0.2, 0.35, 0.45])
        att    = np.random.randint(40, 100) if risk_w=="High" else (
                 np.random.randint(60, 95)  if risk_w=="Medium" else np.random.randint(80,100))
        gpa    = round(np.random.uniform(1.5, 2.5) if risk_w=="High" else (
                       np.random.uniform(2.5, 3.2) if risk_w=="Medium" else
                       np.random.uniform(3.0, 4.0)), 2)
        students.append({
            "id":           i + 1001,
            "name":         f"{random.choice(names_first)} {random.choice(names_last)}",
            "department":   random.choice(DEPARTMENTS),
            "semester":     np.random.randint(1, 9),
            "gpa":          gpa,
            "attendance":   att,
            "risk":         risk_w,
            "risk_score":   round(np.random.uniform(0.6,1.0) if risk_w=="High" else (
                                  np.random.uniform(0.3,0.6) if risk_w=="Medium" else
                                  np.random.uniform(0.0,0.3)), 2),
            "xp":           np.random.randint(100, 2000),
            "mentor":       random.choice(MENTORS) if np.random.rand() > 0.4 else "Unassigned",
            "assignments_done": np.random.randint(30, 100),
            "last_login":   (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(students)

@st.cache_data
def mock_weekly_trend():
    weeks  = [f"W{i}" for i in range(1, 17)]
    high   = [18, 20, 19, 22, 21, 23, 20, 18, 17, 19, 22, 24, 23, 21, 20, 22]
    medium = [38, 36, 37, 35, 34, 33, 35, 37, 36, 34, 33, 31, 32, 34, 35, 33]
    low    = [64, 64, 64, 63, 65, 64, 65, 65, 67, 67, 65, 65, 65, 65, 65, 65]
    return pd.DataFrame({"Week": weeks, "High": high, "Medium": medium, "Low": low})

@st.cache_data
def mock_dept_heatmap():
    sems   = [f"Sem {i}" for i in range(1, 9)]
    data   = np.random.randint(5, 45, (len(DEPARTMENTS), len(sems)))
    return pd.DataFrame(data, index=DEPARTMENTS, columns=sems)

@st.cache_data
def mock_attendance_gpa():
    df = mock_students()
    return df[["name","gpa","attendance","risk","risk_score","department"]]

@st.cache_data
def mock_intervention_list():
    df   = mock_students()
    high = df[df["risk"] == "High"].head(15).copy()
    high["intervention_type"] = np.random.choice(
        ["Counseling", "Extra Classes", "Peer Mentoring", "Parent Meeting", "Academic Warning"],
        len(high))
    high["status"] = np.random.choice(["Pending", "In Progress", "Completed"], len(high))
    return high


# ═══════════════════════════════════════════════════════════
#  PLACEHOLDER API FUNCTIONS  (Backend Integration Points)
# ═══════════════════════════════════════════════════════════

# BACKEND INTEGRATION POINT ─────────────────────────────────
def fetch_college_metrics():
    """
    TODO: Replace with actual API call
    GET /api/v1/metrics/college
    Returns: dict with keys: total_students, high_risk, medium_risk, low_risk,
             avg_gpa, avg_attendance, interventions_active
    """
    df = mock_students()
    return {
        "total_students":       len(df),
        "high_risk":            int((df.risk == "High").sum()),
        "medium_risk":          int((df.risk == "Medium").sum()),
        "low_risk":             int((df.risk == "Low").sum()),
        "avg_gpa":              round(df.gpa.mean(), 2),
        "avg_attendance":       round(df.attendance.mean(), 1),
        "interventions_active": 34,
    }

# BACKEND INTEGRATION POINT ─────────────────────────────────
def fetch_student_risks():
    """
    TODO: Replace with actual API call
    GET /api/v1/students/risks
    Returns: DataFrame with student risk profiles
    """
    return mock_students()

# BACKEND INTEGRATION POINT ─────────────────────────────────
def fetch_student_profile(student_id: int):
    """
    TODO: Replace with actual API call
    GET /api/v1/students/{student_id}/profile
    Returns: dict with full student profile + history
    """
    df  = mock_students()
    row = df[df["id"] == student_id]
    return row.iloc[0].to_dict() if len(row) else None

# BACKEND INTEGRATION POINT ─────────────────────────────────
def assign_mentor(student_id: int, mentor_id: str):
    """
    TODO: Replace with actual API call
    POST /api/v1/mentors/assign
    Body: { student_id, mentor_id }
    Returns: { success: bool, message: str }
    """
    # Mock success
    return {"success": True, "message": f"Mentor {mentor_id} assigned to student {student_id}"}

# BACKEND INTEGRATION POINT ─────────────────────────────────
def fetch_interventions():
    """
    TODO: Replace with actual API call
    GET /api/v1/interventions
    Returns: DataFrame with active interventions
    """
    return mock_intervention_list()

# BACKEND INTEGRATION POINT ─────────────────────────────────
def update_intervention_status(intervention_id: int, status: str):
    """
    TODO: Replace with actual API call
    PATCH /api/v1/interventions/{intervention_id}
    Body: { status }
    Returns: { success: bool }
    """
    return {"success": True}

# BACKEND INTEGRATION POINT ─────────────────────────────────
def send_ai_chat_message(message: str, student_id: int = None):
    """
    TODO: Replace with actual AI backend call
    POST /api/v1/ai/chat
    Body: { message, student_id, context }
    Returns: { response: str }
    """
    responses = [
        "I've analysed your academic profile. Your attendance has improved by 8% this month — keep it up! 📈",
        "Based on your GPA trend, I recommend focusing on your upcoming Math assignment. Want me to create a study plan?",
        "You're currently at Medium risk. The key factors are attendance (72%) and incomplete assignments. Let's work on a strategy.",
        "Great question! Here are 3 resources I recommend for your upcoming exams...",
        "I noticed you haven't logged in for 5 days. Is everything okay? Your mentor Dr. Sharma is available for a quick chat.",
    ]
    return {"response": random.choice(responses)}

# BACKEND INTEGRATION POINT ─────────────────────────────────
def upload_student_csv(file_data):
    """
    TODO: Replace with actual file upload endpoint
    POST /api/v1/data/upload
    Body: multipart/form-data with CSV file
    Returns: { success: bool, records_processed: int, errors: list }
    """
    return {"success": True, "records_processed": 120, "errors": []}


# ═══════════════════════════════════════════════════════════
#  UTILITY / SHARED UI COMPONENTS
# ═══════════════════════════════════════════════════════════

def kpi_card(label, value, delta=None, color="blue"):
    delta_html = ""
    if delta:
        arrow = "↑" if delta >= 0 else "↓"
        clr   = C_GREEN if delta >= 0 else C_RED
        delta_html = f'<div class="kpi-delta" style="color:{clr}">{arrow} {abs(delta)}% vs last month</div>'
    value_colors = {"red": C_RED, "yellow": C_YELLOW, "green": C_GREEN, "blue": C_BLUE}
    vc = value_colors.get(color, C_BLUE)
    st.markdown(f"""
    <div class="kpi-card {color}">
      <div class="kpi-value" style="color:{vc}">{value}</div>
      <div class="kpi-label">{label}</div>
      {delta_html}
    </div>""", unsafe_allow_html=True)

def section_header(icon, title, subtitle=""):
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

def risk_badge(risk):
    cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}
    return f'<span class="badge {cls.get(risk,"badge-low")}">{risk}</span>'

def plotly_dark_layout(fig, height=350, title=""):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color=C_TEXT, size=12),
        title=dict(text=title, font=dict(size=14, color=C_TEXT)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#2D3748"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(gridcolor="#1E293B", zerolinecolor="#1E293B")
    fig.update_yaxes(gridcolor="#1E293B", zerolinecolor="#1E293B")
    return fig


# ═══════════════════════════════════════════════════════════
#  SCREEN: LANDING PAGE
# ═══════════════════════════════════════════════════════════

def render_landing():
    st.markdown('<div class="page-title">AEWIS</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B;font-size:1.05rem;margin-bottom:32px;">Academic Early Warning & Intervention System — Powered by Predictive Intelligence</p>', unsafe_allow_html=True)

    # Upload / Demo row
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        uploaded = st.file_uploader("📂 Upload Student CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            result = upload_student_csv(uploaded)  # BACKEND INTEGRATION POINT
            st.success(f"✅ {result['records_processed']} records processed")
    with col2:
        if st.button("🚀 Load Demo Data", use_container_width=True):
            st.session_state["demo_loaded"] = True
            st.success("Demo data loaded!")

    st.markdown("---")

    # KPI Overview
    metrics = fetch_college_metrics()   # BACKEND INTEGRATION POINT
    section_header("📊", "System Overview", "Live snapshot of student risk distribution")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Total Students",     metrics["total_students"],   delta=+3,  color="blue")
    with c2: kpi_card("High Risk",          metrics["high_risk"],        delta=+12, color="red")
    with c3: kpi_card("Medium Risk",        metrics["medium_risk"],      delta=-4,  color="yellow")
    with c4: kpi_card("Low Risk",           metrics["low_risk"],         delta=+2,  color="green")

    st.markdown("---")

    # Role description cards
    section_header("👥", "Who Uses AEWIS?")
    r1, r2, r3 = st.columns(3)

    def role_card(col, icon, role, desc, color):
        with col:
            st.markdown(f"""
            <div class="kpi-card {color}" style="min-height:160px;">
              <div style="font-size:2.5rem">{icon}</div>
              <div style="font-size:1.1rem;font-weight:700;margin:8px 0 4px">{role}</div>
              <div style="font-size:0.85rem;color:#94A3B8">{desc}</div>
            </div>""", unsafe_allow_html=True)

    role_card(r1, "🏛️", "Administrator",
              "College-wide risk analytics, mentor assignment, intervention oversight, and policy dashboards.",
              "blue")
    role_card(r2, "👩‍🏫", "Teacher",
              "Monitor your students, trigger interventions, track productivity, and view per-class analytics.",
              "green")
    role_card(r3, "🎓", "Student",
              "View your personal risk score, XP level, AI-powered study assistant, and progress metrics.",
              "yellow")

    # Quick trend
    st.markdown("---")
    section_header("📈", "Risk Trend (Current Semester)")
    trend = mock_weekly_trend()
    fig = go.Figure()
    for level, color in [("High", C_RED), ("Medium", C_YELLOW), ("Low", C_GREEN)]:
        fig.add_trace(go.Scatter(x=trend["Week"], y=trend[level], name=level,
                                 line=dict(color=color, width=2.5), mode="lines+markers",
                                 marker=dict(size=5)))
    fig = plotly_dark_layout(fig, height=280, title="Weekly At-Risk Student Counts")
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
#  ADMIN SCREENS
# ═══════════════════════════════════════════════════════════

def render_admin_overview():
    section_header("🏛️", "College Overview", "Institution-wide risk intelligence dashboard")

    metrics = fetch_college_metrics()  # BACKEND INTEGRATION POINT
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Students",          metrics["total_students"],        delta=+3,  color="blue")
    with c2: kpi_card("High Risk",         metrics["high_risk"],             delta=+12, color="red")
    with c3: kpi_card("Medium Risk",       metrics["medium_risk"],           delta=-4,  color="yellow")
    with c4: kpi_card("Avg GPA",           metrics["avg_gpa"],               delta=-2,  color="blue")
    with c5: kpi_card("Active Interventions", metrics["interventions_active"], delta=+8, color="green")

    st.markdown("---")
    col_heatmap, col_table = st.columns([3, 2])

    with col_heatmap:
        section_header("🔥", "Risk Heatmap", "At-risk count by Department × Semester")
        hm = mock_dept_heatmap()
        fig = px.imshow(hm, color_continuous_scale=["#0F172A", C_YELLOW, C_RED],
                        labels=dict(x="Semester", y="Department", color="At-Risk"))
        fig.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Space Grotesk", color=C_TEXT, size=11),
                          margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        section_header("⚠️", "Top 10 At-Risk Students")
        df   = fetch_student_risks()  # BACKEND INTEGRATION POINT
        top  = df.nlargest(10, "risk_score")[["name","department","gpa","attendance","risk_score","risk"]].copy()
        top["Risk"] = top["risk"].apply(lambda r: risk_badge(r))
        top = top.drop("risk", axis=1)
        top.columns = ["Name","Dept","GPA","Att%","Score","Risk"]
        st.markdown(top.to_html(escape=False, index=False), unsafe_allow_html=True)

def render_admin_analytics():
    section_header("📊", "Risk Analytics", "Deep-dive into student risk patterns")

    df = fetch_student_risks()  # BACKEND INTEGRATION POINT
    trend = mock_weekly_trend()

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        # Pie
        risk_cnt = df["risk"].value_counts().reset_index()
        risk_cnt.columns = ["Risk Level", "Count"]
        fig = px.pie(risk_cnt, names="Risk Level", values="Count",
                     color="Risk Level",
                     color_discrete_map={"High": C_RED, "Medium": C_YELLOW, "Low": C_GREEN},
                     hole=0.45)
        fig = plotly_dark_layout(fig, height=320, title="Risk Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with row1_c2:
        # Bar – by dept
        dept_risk = df.groupby(["department","risk"]).size().reset_index(name="count")
        fig = px.bar(dept_risk, x="department", y="count", color="risk",
                     color_discrete_map={"High": C_RED, "Medium": C_YELLOW, "Low": C_GREEN},
                     barmode="stack")
        fig = plotly_dark_layout(fig, height=320, title="Risk by Department")
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        # Line – weekly trend
        fig = go.Figure()
        for level, clr in [("High", C_RED), ("Medium", C_YELLOW), ("Low", C_GREEN)]:
            fig.add_trace(go.Scatter(x=trend["Week"], y=trend[level], name=level,
                                     line=dict(color=clr, width=2.5), fill="tozeroy",
                                     fillcolor=f"rgba({','.join(str(int(clr.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.07)"))
        fig = plotly_dark_layout(fig, height=300, title="Risk Trend Over Semester")
        st.plotly_chart(fig, use_container_width=True)

    with row2_c2:
        # Scatter – GPA vs Attendance
        fig = px.scatter(df, x="attendance", y="gpa", color="risk",
                         color_discrete_map={"High": C_RED, "Medium": C_YELLOW, "Low": C_GREEN},
                         hover_data=["name","department"],
                         size_max=8, opacity=0.75)
        fig = plotly_dark_layout(fig, height=300, title="GPA vs Attendance")
        st.plotly_chart(fig, use_container_width=True)

def render_admin_mentors():
    section_header("🔗", "Mentor Assignment", "Assign faculty mentors to at-risk students")

    df = fetch_student_risks()  # BACKEND INTEGRATION POINT
    high_med = df[df["risk"].isin(["High","Medium"])].copy().reset_index(drop=True)

    st.info(f"🔔  {len(high_med)} students require mentor assignment or review.")

    st.markdown("**Bulk Assignment Panel**")
    col_filter, col_bulk, _ = st.columns([2, 2, 4])
    with col_filter:
        dept_filter = st.selectbox("Filter by Dept", ["All"] + DEPARTMENTS)
    with col_bulk:
        bulk_mentor = st.selectbox("Bulk assign mentor", MENTORS)

    if dept_filter != "All":
        high_med = high_med[high_med["department"] == dept_filter]

    st.markdown("---")

    # Simulate session state for mentor selections
    if "mentor_selections" not in st.session_state:
        st.session_state["mentor_selections"] = {}

    headers = ["ID", "Name", "Dept", "Risk", "GPA", "Att%", "Assign Mentor", "Action"]
    header_cols = st.columns([1, 2, 2, 1, 1, 1, 2, 1])
    for h, c in zip(headers, header_cols):
        c.markdown(f"**{h}**")

    st.markdown('<div style="border-bottom:1px solid #2D3748;margin-bottom:8px;"></div>', unsafe_allow_html=True)

    for _, row in high_med.head(12).iterrows():
        sid = row["id"]
        cols = st.columns([1, 2, 2, 1, 1, 1, 2, 1])
        cols[0].write(str(sid))
        cols[1].write(row["name"])
        cols[2].write(row["department"])
        cols[3].markdown(risk_badge(row["risk"]), unsafe_allow_html=True)
        cols[4].write(str(row["gpa"]))
        cols[5].write(str(row["attendance"]) + "%")
        current = st.session_state["mentor_selections"].get(sid, row["mentor"])
        choice  = cols[6].selectbox("", MENTORS + ["Unassigned"], index=MENTORS.index(current) if current in MENTORS else len(MENTORS), key=f"mentor_{sid}", label_visibility="collapsed")
        if cols[7].button("✓", key=f"assign_{sid}"):
            result = assign_mentor(sid, choice)  # BACKEND INTEGRATION POINT
            st.session_state["mentor_selections"][sid] = choice
            st.toast(f"✅ {row['name']} → {choice}", icon="🎓")

    st.markdown("---")
    if st.button("💾 Apply Bulk Assignment", use_container_width=False):
        for _, row in high_med.iterrows():
            assign_mentor(row["id"], bulk_mentor)  # BACKEND INTEGRATION POINT
        st.success(f"✅ Bulk assigned: {bulk_mentor} to {len(high_med)} students")


# ═══════════════════════════════════════════════════════════
#  TEACHER SCREENS
# ═══════════════════════════════════════════════════════════

def render_teacher_dashboard():
    section_header("👩‍🏫", "Student Dashboard", "Your class at a glance")

    sidebar_col, main_col = st.columns([1, 3])

    with sidebar_col:
        st.markdown('<div class="kpi-card blue" style="padding:16px">', unsafe_allow_html=True)
        st.markdown("**📅 Today**")
        st.markdown(f"<small style='color:#94A3B8'>{datetime.now().strftime('%A, %B %d')}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kpi-card green">', unsafe_allow_html=True)
        st.markdown("**📝 Quick Notes**")
        st.text_area("", placeholder="Type class notes...", height=80, key="teacher_notes", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kpi-card yellow">', unsafe_allow_html=True)
        st.markdown("**⏱ Focus Timer**")
        timer_mins = st.slider("Minutes", 5, 60, 25, key="timer_slider")
        if st.button(f"▶ Start {timer_mins}min", use_container_width=True):
            st.info(f"Timer started for {timer_mins} minutes")
        st.markdown('</div>', unsafe_allow_html=True)

    with main_col:
        df = fetch_student_risks()  # BACKEND INTEGRATION POINT
        filter_risk = st.pills("Filter by Risk", ["All", "High", "Medium", "Low"], default="All", key="tc_risk_filter")
        show_df = df if filter_risk == "All" else df[df["risk"] == filter_risk]

        cols_per_row = 3
        rows = [list(show_df.head(12).iterrows())[i:i+cols_per_row] for i in range(0, min(12, len(show_df)), cols_per_row)]
        for row_group in rows:
            card_cols = st.columns(cols_per_row)
            for col, (_, student) in zip(card_cols, row_group):
                with col:
                    risk_clr = RISK_COLORS[student["risk"]]
                    xp_pct   = min(100, student["xp"] // 20)
                    level    = student["xp"] // 200 + 1
                    st.markdown(f"""
                    <div class="student-card">
                      <div style="display:flex;justify-content:space-between;align-items:start">
                        <div>
                          <div style="font-weight:600;font-size:0.9rem">{student['name']}</div>
                          <div style="font-size:0.75rem;color:#64748B">{student['department']}</div>
                        </div>
                        <div>{risk_badge(student['risk'])}</div>
                      </div>
                      <div style="margin-top:10px;display:flex;gap:16px;font-size:0.8rem">
                        <span>GPA <b style="color:{risk_clr}">{student['gpa']}</b></span>
                        <span>Att <b style="color:{risk_clr}">{student['attendance']}%</b></span>
                      </div>
                      <div style="margin-top:8px;font-size:0.75rem;color:#94A3B8">
                        ⭐ Level {level} · {student['xp']} XP
                      </div>
                      <div class="xp-bar-bg">
                        <div class="xp-bar-fill" style="width:{xp_pct}%;background:{risk_clr}"></div>
                      </div>
                    </div>""", unsafe_allow_html=True)

def render_teacher_interventions():
    section_header("🚨", "Intervention List", "Manage active early warning interventions")

    if "intervention_states" not in st.session_state:
        st.session_state["intervention_states"] = {}

    df = fetch_interventions()  # BACKEND INTEGRATION POINT

    # Metric strip
    total  = len(df)
    done   = sum(1 for _, r in df.iterrows() if st.session_state["intervention_states"].get(r["id"], r["status"]) == "Completed")
    active = total - done
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total Interventions", total,  color="blue")
    with c2: kpi_card("Active",              active, color="red")
    with c3: kpi_card("Completed",           done,   color="green")

    st.markdown("---")

    for _, row in df.iterrows():
        sid    = row["id"]
        status = st.session_state["intervention_states"].get(sid, row["status"])
        status_clr = {"Pending": C_YELLOW, "In Progress": C_BLUE, "Completed": C_GREEN}.get(status, C_TEXT)

        with st.container():
            ic1, ic2, ic3, ic4, ic5 = st.columns([3, 2, 2, 2, 2])
            ic1.markdown(f"**{row['name']}** <small style='color:#64748B'>— {row['department']}</small>", unsafe_allow_html=True)
            ic2.markdown(risk_badge(row["risk"]), unsafe_allow_html=True)
            ic3.write(row["intervention_type"])
            ic4.markdown(f'<span style="color:{status_clr};font-weight:600">{status}</span>', unsafe_allow_html=True)

            new_status = ic5.selectbox("", ["Pending","In Progress","Completed"],
                                       index=["Pending","In Progress","Completed"].index(status),
                                       key=f"int_{sid}", label_visibility="collapsed")
            if new_status != status:
                update_intervention_status(sid, new_status)  # BACKEND INTEGRATION POINT
                st.session_state["intervention_states"][sid] = new_status
                st.rerun()

            st.markdown('<div style="border-bottom:1px solid #1E293B;margin:4px 0"></div>', unsafe_allow_html=True)

def render_teacher_analytics():
    section_header("📈", "Teacher Analytics", "Trends and performance metrics for your students")

    df    = fetch_student_risks()  # BACKEND INTEGRATION POINT
    trend = mock_weekly_trend()

    ca, cb = st.columns(2)
    with ca:
        fig = px.histogram(df, x="gpa", color="risk", nbins=20,
                           color_discrete_map={"High": C_RED, "Medium": C_YELLOW, "Low": C_GREEN},
                           barmode="overlay", opacity=0.75)
        fig = plotly_dark_layout(fig, height=300, title="GPA Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with cb:
        sem_gpa = df.groupby("semester")["gpa"].mean().reset_index()
        fig = px.line(sem_gpa, x="semester", y="gpa", markers=True,
                      line_shape="spline")
        fig.update_traces(line_color=C_BLUE, marker=dict(color=C_BLUE, size=8))
        fig = plotly_dark_layout(fig, height=300, title="Avg GPA by Semester")
        st.plotly_chart(fig, use_container_width=True)

    cc, cd = st.columns(2)
    with cc:
        att_dept = df.groupby("department")["attendance"].mean().reset_index().sort_values("attendance")
        colors = [C_RED if v < 70 else C_YELLOW if v < 85 else C_GREEN for v in att_dept["attendance"]]
        fig = go.Figure(go.Bar(x=att_dept["attendance"], y=att_dept["department"],
                               orientation="h", marker_color=colors))
        fig = plotly_dark_layout(fig, height=300, title="Avg Attendance by Department")
        st.plotly_chart(fig, use_container_width=True)

    with cd:
        fig = go.Figure()
        for level, clr in [("High", C_RED), ("Medium", C_YELLOW), ("Low", C_GREEN)]:
            fig.add_trace(go.Bar(x=trend["Week"][-8:], y=trend[level][-8:],
                                 name=level, marker_color=clr))
        fig.update_layout(barmode="stack")
        fig = plotly_dark_layout(fig, height=300, title="Weekly Risk Count (Last 8 Weeks)")
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
#  STUDENT SCREENS
# ═══════════════════════════════════════════════════════════

def render_student_dashboard():
    section_header("🎓", "My Academic Dashboard", "Your personalized performance snapshot")

    # Mock: logged-in student = first high-risk student
    df      = fetch_student_risks()  # BACKEND INTEGRATION POINT
    profile = df[df["risk"] == "High"].iloc[0].to_dict()

    # Profile header
    risk_clr = RISK_COLORS[profile["risk"]]
    xp_pct   = min(100, profile["xp"] // 20)
    level    = profile["xp"] // 200 + 1

    st.markdown(f"""
    <div class="kpi-card blue" style="display:flex;align-items:center;gap:24px;padding:24px">
      <div style="font-size:4rem">🎓</div>
      <div style="flex:1">
        <div style="font-size:1.4rem;font-weight:700">{profile['name']}</div>
        <div style="color:#64748B;font-size:0.9rem">{profile['department']} · Semester {profile['semester']}</div>
        <div style="margin-top:8px;display:flex;gap:12px;align-items:center">
          {risk_badge(profile['risk'])}
          <span style="color:#94A3B8;font-size:0.8rem">Last login: {profile['last_login']}</span>
        </div>
      </div>
      <div style="text-align:right">
        <div style="font-size:2rem;font-weight:800;color:{C_BLUE}">Lvl {level}</div>
        <div style="font-size:0.8rem;color:#94A3B8">{profile['xp']} / 2000 XP</div>
        <div class="xp-bar-bg" style="width:160px;margin-top:6px">
          <div class="xp-bar-fill" style="width:{xp_pct}%;background:{C_BLUE}"></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)
    gpa_clr = "green" if profile["gpa"] >= 3.0 else "yellow" if profile["gpa"] >= 2.5 else "red"
    att_clr = "green" if profile["attendance"] >= 85 else "yellow" if profile["attendance"] >= 70 else "red"
    with c1: kpi_card("GPA",           profile["gpa"],               color=gpa_clr)
    with c2: kpi_card("Attendance",    f"{profile['attendance']}%",  color=att_clr)
    with c3: kpi_card("Assignments Done", f"{profile['assignments_done']}%", color="blue")
    with c4: kpi_card("Risk Score",    profile["risk_score"],        color="red" if profile["risk_score"] > 0.6 else "yellow")

    st.markdown("---")

    # Progress radar + achievement badges
    ra, rb = st.columns([2, 1])
    with ra:
        categories = ["Attendance", "GPA", "Assignments", "Participation", "Punctuality", "Engagement"]
        values     = [profile["attendance"] / 100, profile["gpa"] / 4,
                      profile["assignments_done"] / 100, 0.65, 0.70, 0.55]
        fig = go.Figure(go.Scatterpolar(r=values, theta=categories, fill="toself",
                                        line_color=C_BLUE, fillcolor="rgba(59,130,246,0.15)"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1],
                                                      gridcolor="#2D3748", color="#64748B"),
                                     angularaxis=dict(gridcolor="#2D3748")),
                          height=320, paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Space Grotesk", color=C_TEXT))
        st.plotly_chart(fig, use_container_width=True)

    with rb:
        st.markdown("**🏆 Achievements**")
        badges = [
            ("🔥", "7-Day Streak",    "green",  True),
            ("📚", "Book Worm",       "blue",   True),
            ("⚡", "Quick Learner",   "yellow", True),
            ("🎯", "Perfect Score",   "green",  False),
            ("🤝", "Team Player",     "blue",   False),
        ]
        for icon, name, clr, earned in badges:
            opacity = "1" if earned else "0.25"
            st.markdown(f"""
            <div style="opacity:{opacity};display:flex;align-items:center;gap:10px;
                        background:#1E293B;border-radius:8px;padding:8px 12px;margin-bottom:6px">
              <span style="font-size:1.2rem">{icon}</span>
              <span style="font-size:0.85rem;font-weight:500">{name}</span>
            </div>""", unsafe_allow_html=True)

def render_student_ai_chat():
    section_header("🤖", "AI Study Assistant", "Your personal academic AI advisor")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "bot", "content": "Hello! I'm your AEWIS AI assistant 🤖 I can help you with study strategies, track your progress, and provide personalised recommendations. How can I help you today?"}
        ]

    # Chat display
    st.markdown('<div style="background:#0B1120;border-radius:12px;padding:20px;min-height:400px;max-height:400px;overflow-y:auto;border:1px solid #1E293B">', unsafe_allow_html=True)
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px">
              <div class="robot-icon">🤖</div>
              <div class="chat-bot">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input
    st.markdown("<br>", unsafe_allow_html=True)
    quick_prompts = ["📊 Show my risk factors", "📅 Create study plan", "📈 Attendance tips", "🎯 Improve GPA"]
    prompt_cols = st.columns(len(quick_prompts))
    for col, qp in zip(prompt_cols, quick_prompts):
        if col.button(qp, use_container_width=True):
            st.session_state["chat_history"].append({"role": "user", "content": qp})
            resp = send_ai_chat_message(qp)  # BACKEND INTEGRATION POINT
            st.session_state["chat_history"].append({"role": "bot", "content": resp["response"]})
            st.rerun()

    user_input = st.chat_input("Ask me anything about your academics...")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        resp = send_ai_chat_message(user_input)  # BACKEND INTEGRATION POINT
        st.session_state["chat_history"].append({"role": "bot", "content": resp["response"]})
        st.rerun()


# ═══════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding:16px 0;border-bottom:1px solid #1E293B;margin-bottom:16px">
          <div style="font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#3B82F6,#10B981);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent">
            AEWIS
          </div>
          <div style="font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase">
            Early Warning System
          </div>
        </div>""", unsafe_allow_html=True)

        # Role selector
        role = st.selectbox("👤 Role", ["🏛️ Admin", "👩‍🏫 Teacher", "🎓 Student"], label_visibility="visible")

        st.markdown('<div style="border-bottom:1px solid #1E293B;margin:12px 0"></div>', unsafe_allow_html=True)

        screen = None

        if "Admin" in role:
            st.markdown('<div style="font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">ADMIN</div>', unsafe_allow_html=True)
            if st.button("📊  College Overview",      use_container_width=True): st.session_state["screen"] = "admin_overview"
            if st.button("📈  Risk Analytics",        use_container_width=True): st.session_state["screen"] = "admin_analytics"
            if st.button("🔗  Mentor Assignment",     use_container_width=True): st.session_state["screen"] = "admin_mentors"

        elif "Teacher" in role:
            st.markdown('<div style="font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">TEACHER</div>', unsafe_allow_html=True)
            if st.button("👥  Student Dashboard",     use_container_width=True): st.session_state["screen"] = "teacher_dashboard"
            if st.button("🚨  Intervention List",     use_container_width=True): st.session_state["screen"] = "teacher_interventions"
            if st.button("📊  Teacher Analytics",     use_container_width=True): st.session_state["screen"] = "teacher_analytics"

        elif "Student" in role:
            st.markdown('<div style="font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">STUDENT</div>', unsafe_allow_html=True)
            if st.button("🎓  My Dashboard",          use_container_width=True): st.session_state["screen"] = "student_dashboard"
            if st.button("🤖  AI Assistant",          use_container_width=True): st.session_state["screen"] = "student_ai"

        st.markdown("---")
        if st.button("🏠  Home / Landing",            use_container_width=True): st.session_state["screen"] = "landing"

        # Status footer
        st.markdown("""
        <div style="position:fixed;bottom:16px;left:0;width:260px;padding:0 16px">
          <div style="background:#0B1120;border:1px solid #1E293B;border-radius:8px;padding:10px 12px">
            <div style="font-size:0.7rem;color:#64748B">SYSTEM STATUS</div>
            <div style="font-size:0.8rem;color:#10B981;margin-top:2px">● All systems operational</div>
            <div style="font-size:0.7rem;color:#64748B;margin-top:4px">v1.0.0 · Demo Mode</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  MAIN ROUTER
# ═══════════════════════════════════════════════════════════

def main():
    if "screen" not in st.session_state:
        st.session_state["screen"] = "landing"

    render_sidebar()

    screen = st.session_state.get("screen", "landing")

    route_map = {
        "landing":               render_landing,
        "admin_overview":        render_admin_overview,
        "admin_analytics":       render_admin_analytics,
        "admin_mentors":         render_admin_mentors,
        "teacher_dashboard":     render_teacher_dashboard,
        "teacher_interventions": render_teacher_interventions,
        "teacher_analytics":     render_teacher_analytics,
        "student_dashboard":     render_student_dashboard,
        "student_ai":            render_student_ai_chat,
    }

    render_fn = route_map.get(screen, render_landing)
    render_fn()


if __name__ == "__main__":
    main()
