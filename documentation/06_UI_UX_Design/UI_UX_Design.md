# AEWIS UI/UX Design Plan - Streamlit Hackathon Demo

**Version:** 1.0 (Demo-Optimized)  
**Date:** February 24, 2026  
**Goal:** Maximum judge comprehension in 60 seconds  
**Principle:** Clarity > Polish > Features  

***

## 1. Admin Dashboard Layout

```
HEADER (Full Width)
┌─ Academic Early Warning System ────────────────────────┐
│ Uploaded: 200 students | High Risk: 42 👥 | Physics ↓  │
└────────────────────────────────────────────────────────┘

MAIN CONTENT (2-Column)
┌─ LEFT: KPIs (30%) ─────┐ ┌─ RIGHT: HEATMAP (70%) ─────┐
│ High Risk: 42 🔴       │ │ [Plotly imshow]            │
│ Medium: 18 🟡          │ │ Red=High, Green=Low        │
│ Low: 140 🟢            │ │ Subjects vs Students       │
│                        │ │ Physics cluster = CRISIS   │
│ [HIGH RISK TABLE]      │ │                            │
│ S101 Math Decline+Att  │ │                            │
│ S104 Phys Attendance   │ │                            │
└────────────────────────┘ └────────────────────────────┘
```

**Streamlit Code:**
```python
col1, col2 = st.columns([1, 2])
with col1:
    st.metric("High Risk", 42, delta="-15%")
    st.dataframe(high_risk_table, use_container_width=True)
with col2:
    st.plotly_chart(heatmap, use_container_width=True)
```

***

## 2. Teacher Dashboard Layout

```
HEADER (Same as Admin)
┌─ Ms. Sharma (Math) ── At-Risk Students ─────────────────┐
│ My High Risks: 8 👥 | Intervention Success: 62% 📈    │
└────────────────────────────────────────────────────────┘

MAIN CONTENT (Single Column - Simplicity)
┌─ INTERVENTION LIST ──────────────────────────────────────┐
│ [Toggle] S101  Math  Decline+Att   Quiz:72→54 [Mark ✅]  │
│ [Toggle] S105  Math  All Signals   Quiz:55→42 [Mark ✅]  │
│ [Toggle] S112  Math  Attendance    65% attend     [Mark] │
│                                                         │
│ Impact: Risks reduced from 12 → 8 after interventions   │
└─────────────────────────────────────────────────────────┘
```

**Key:** One actionable list. No distractions.

***

## 3. Interaction Flow

```
1. LANDING → CSV Upload (st.file_uploader center stage)
2. PROCESS → "✅ 200 students analyzed" + Auto Admin view
3. EXPLORE → Click "High Risk" filter → Table updates
4. SWITCH → Sidebar "Teacher View" → Filtered list appears
5. ACT → Toggle checkboxes → Live risk count drops
6. INVITE → "Drag your CSV here → See your risks instantly"
```

**Golden Rule:** Every click shows *immediate visual feedback.*

***

## 4. Chart Types and Heatmap Design

| Visual | Type | Purpose | Streamlit Code |
|--------|------|---------|---------------|
| **Risk Distribution** | Pie/Donut | Instant risk breakdown | `px.pie(values=[42,18,140], names=['High','Med','Low'])` |
| **Subject Heatmap** | `px.imshow` | Crisis clusters | `px.imshow(risk_matrix, color_continuous_scale='RdYlGn_r')` |
| **Risk Trend** | Line (future) | Score declines | `px.line(df, x='Quiz', y='Score', color='Risk')` |

**Heatmap Perfection:**
```python
risk_matrix = risk_df.pivot(index='StudentID', columns='Subject', values='risk_level')
fig = px.imshow(risk_matrix, color_continuous_scale='RdYlGn_r', 
                title="🔴 Red = High Risk Subjects")
```

**Color Magic:** Red draws eyes instantly → Judges see Physics crisis.

***

## 5. Visual Hierarchy Strategy

```
TIER 1 - IMMEDIATE (First 3 seconds)
├── Big header: "42 High Risk Students"
├── Red heatmap cluster
└── KPI cards with delta badges

TIER 2 - SCAN (Next 10 seconds)  
├── Risk reason column
├── Subject with most red
└── Intervention success %

TIER 3 - DETAIL (Click to expand)
├── Full student table
├── Individual score trends
└── Historical interventions
```

**Streamlit Priority:**
```python
st.title("High Risk: 42 👥")  # TIER 1
st.metric("Risk Reduction", "15%", delta_color="normal")  # TIER 1
st.plotly_chart(heatmap)  # TIER 1
```

***

## 6. Demo Storytelling Flow

```
SCREEN 1 (0-60s): "PROBLEM + UPLOAD"
"Colleges collect data → store → forget. Watch this..."
[Upload CSV → Instant metrics + heatmap]

SCREEN 2 (60-120s): "ADMIN VIEW"  
"Admin sees Physics is on fire. 42 students need help NOW."
[Point to red cluster → Filter high-risk table]

SCREEN 3 (120-180s): "TEACHER ACTION"
"Ms.Sharma gets HER list only. One click to intervene."
[Role switch → Toggle → Live delta: "42→36 risks"]

SCREEN 4 (180-240s): "JUDGE INVITE"
"Your CSV? Drag it here → Instant college insights."
[Point to uploader → QR code]
```

**Narrative Arc:** Problem → Discovery → Action → Impact → Personalization

***

## 7. What to Avoid in UI

| ❌ NEVER DO | Why It Kills Demos |
|------------|------------------|
| **Multiple Tabs** | Judges miss role switch |
| **Tiny Text** | Can't read from 5m away |
| **Static Charts** | No interactivity = boring |
| **10+ Visuals** | Cognitive overload |
| **Login Screens** | Friction kills flow |
| **Mobile Layout** | Judges use laptops |
| **Empty States** | "Nothing to demo" panic |

**Streamlit Traps:**
```python
# ❌ BAD: Too many elements
st.write("Metric 1"); st.write("Metric 2")  # Scrolls

# ✅ GOOD: Columns + containers
col1.metric("Risks", 42); col2.metric("Success", "62%")
```

***

## 8. 5-Minute Demo Optimization Tips

**Physical Demo Flow:**
```
1. OPEN app (pre-loaded, browser maximized)
2. HIT "Load Demo Data" button (pre-made CSV)
3. WALK THROUGH 30s pitch WHILE screen shows upload→results
4. PHYSICALLY POINT to heatmap red zones (laser pointer effect)
5. VERBALLY CALL metrics BEFORE they appear ("Watch for 42...")
6. PAUSE after each major interaction (let judges absorb)
7. END with QR code + "Try your data live!"
```

**Screen Real Estate:**
```
85% Content | 15% Streamlit chrome
No browser tabs | Fullscreen F11
1440p minimum | 32" screen ideal
```

**Audio Cues:**
- "Watch this red cluster appear..."
- "Risk count DROPS from 42..."
- "Teacher sees only HER students..."
- "Your CSV works instantly!"

***

## Streamlit UI Skeleton (Copy-Paste Ready)

```python
# HEADER
st.set_page_config(layout="wide", page_title="AEWIS")
st.title("🔴 42 High Risk Students Detected")

# UPLOAD
uploaded = st.file_uploader("CSV", "Upload college data")

# DASHBOARDS
col1, col2 = st.columns([1,2])
with col1:
    st.metric("High Risk", 42, "-15%")
    st.dataframe(risk_table)
with col2:
    st.plotly_chart(heatmap)

# TEACHER ACTION
if st.button("Switch to Teacher View"):
    st.session_state.role = "teacher"
```

***

## Demo Success Metrics

```
✅ Judges say "Oh, I see Physics is the problem!"
✅ Can follow flow without explanation  
✅ Risk count changes live on toggle
✅ "Try my CSV" invite feels natural
✅ Leaves wanting to test their data
```

**Status: VISUALLY READY.** Heatmap = killer feature. Build this exact layout. Judges will remember the red Physics cluster. Demo wins.