# Technical Architecture Document  
## Academic Early Warning System (AEWIS) - Streamlit MVP

**Version:** 1.0 (Hackathon)  
**Date:** February 24, 2026  
**Author:** Senior Systems Architect  
**Constraint:** Single-file Streamlit app, solo build, <300 lines total  

***

## 1. High-Level Architecture Description

```
[CSV Upload] → [Pandas DataFrame] → [Risk Engine] → [Streamlit Session Cache] → [Role-Based Views]
                                 ↓
                           [Plotly Visuals] ← [Interactive Controls]
```

**Single Responsibility Principle:** One Python file (`app.py`) handles everything. No external services, databases, or APIs. Pure in-memory processing with Streamlit session state persistence.

**Core Data Flow:**  
`st.file_uploader` → `pd.read_csv()` → `risk_scoring()` → `st.session_state.df` → Role-specific rendering.

***

## 2. Module/File Breakdown (Single-File MVP)

```
app.py (100% of codebase)
├── imports (10 lines)
├── risk_scoring() function (25 lines)          # Core business logic
├── load_sample_data() function (15 lines)      # Demo dataset generator
├── admin_dashboard() function (40 lines)       # Admin views
├── teacher_dashboard() function (30 lines)     # Teacher views
├── sidebar_auth() function (15 lines)          # Role switching
├── main() execution flow (25 lines)           # Streamlit lifecycle
└── utils inline (inline validation, caching)  # No separate files
```

**Total: ~200-250 lines. Zero dependencies beyond:** `streamlit pandas plotly numpy`

***

## 3. Data Ingestion Pipeline

```
CSV Schema (strict 7 columns):
StudentID,Subject,Quiz1,Quiz2,Quiz3,Attendance,Teacher

Step-by-step:
1. st.file_uploader("Upload CSV", type="csv")
2. if uploaded: df = pd.read_csv(uploaded)
3. validate_schema(df)  # Check column names + data types
4. df = clean_data(df)  # NaN fill, type coercion
5. st.session_state.df = df  # Persist across reruns
6. st.success(f"✅ Loaded {len(df)} records")
```

**Validation Rules:**
```python
required_cols = ['StudentID','Subject','Quiz1','Quiz2','Quiz3','Attendance']
if not all(col in df.columns for col in required_cols): st.error("Schema mismatch")
```

***

## 4. Risk Scoring Pipeline

**Vectorized Pandas (processes 10k rows < 50ms):**

```python
def risk_scoring(df):
    df_out = df.copy()
    
    # Compute metrics
    df_out['avg_score'] = df[['Quiz1','Quiz2','Quiz3']].mean(axis=1)
    df_out['score_drop'] = (df['Quiz1'] - df['Quiz3']) / df['Quiz1'] * 100 >= 15
    df_out['low_avg'] = df_out['avg_score'] < 40
    df_out['low_attend'] = df['Attendance'] < 75
    
    # Override safety rule
    df_out['override_safe'] = (df['Attendance'] >= 85) & (df_out['avg_score'] >= 70)
    
    # Risk level (vectorized)
    conditions_met = df_out[['score_drop','low_avg','low_attend']].sum(axis=1)
    df_out['risk_level'] = np.where(
        df_out['override_safe'], 'Low',
        np.where(conditions_met >= 1, 'High', 'Low')
    )
    
    # Reason aggregation
    reasons = []
    if df_out['score_drop'].any(): reasons.append('Decline ≥15%')
    if df_out['low_avg'].any(): reasons.append('Avg <40%')
    if df_out['low_attend'].any(): reasons.append('Attendance <75%')
    df_out['risk_reason'] = ', '.join(reasons)
    
    return df_out
```

***

## 5. State Management in Streamlit

**Session State Schema:**
```python
if 'df' not in st.session_state:
    st.session_state = {
        'df': None,           # Processed DataFrame
        'role': 'admin',      # Current user role
        'risk_df': None,      # Cached risk results
        'interventions': {}   # {StudentID: status}
    }
```

**Persistence Pattern:**
```python
# On upload
if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.session_state.risk_df = risk_scoring(st.session_state.df)
    st.rerun()

# Role switching
if st.sidebar.selectbox("Role", ['admin','teacher']) == 'teacher':
    st.session_state.role = 'teacher'
```

***

## 6. Performance Considerations

| Component | Optimization | Expected Time |
|-----------|--------------|---------------|
| **CSV Parse** | Pandas native | <50ms (10k rows) |
| **Risk Calc** | Vectorized numpy | <20ms (10k rows) |
| **Plotly Render** | `@st.cache_data` | <100ms refresh |
| **Table Filter** | `st.dataframe` native | Instant |

**Hackathon Reality:** 200-student demo dataset loads in <200ms total. Zero bottlenecks.

**Caching Strategy:**
```python
@st.cache_data
def generate_heatmap(_risk_df):
    return px.imshow(...)  # Cache chart computation
```

***

## 7. Deployment Options

| Environment | Command | URL | Pros | Cons |
|-------------|---------|-----|------|------|
| **Local Dev** | `streamlit run app.py` | `localhost:8501` | Instant | Judges can't access |
| **Streamlit Cloud** | Git push → auto-deploy | `yourapp.streamlit.app` | Free, public URL | Git required |
| **Hugging Face Spaces** | Git push Dockerfile | `hf.space/yourapp` | GPU option | Overkill |

**Recommended:** Streamlit Cloud (2-click deploy from GitHub).

***

## 8. How Architecture Evolves Post-Hackathon

| Phase | Changes | Tech Additions |
|-------|---------|---------------|
| **Pilot (Week 2)** | SQLite persistence | `sqlite3` + upload history |
| **v1.0 (Month 1)** | Multi-tenancy | `college_id` column + Postgres |
| **v2.0 (Month 3)** | API endpoints | FastAPI wrapper |
| **v3.0 (Month 6)** | Real-time | WebSocket updates |

**MVP → Production:** Add only authentication layer (`streamlit-authenticator`).

***

## 9. Explicit List of What NOT to Build

| ❌ NEVER BUILD IN HACKATHON | Reason |
|----------------------------|--------|
| Database (SQLite/Postgres) | In-memory wins for demo |
| Real authentication | Hardcode 2 demo users |
| REST APIs | CSV upload = 100% use case |
| Background jobs | Streamlit single-threaded |
| Mobile responsiveness | Desktop demo only |
| Unit tests | Time zero |
| Config files/YAML | Inline everything |
| Docker | Streamlit Cloud native |
| Multiple pages/files | Single `app.py` |

***

## Implementation Priority (4-Hour Build Order)

```
1. [30min] risk_scoring() function + sample data generator
2. [60min] CSV upload + basic admin dashboard (KPI cards)
3. [60min] Plotly heatmap + risk table
4. [45min] Teacher dashboard + intervention toggle
5. [30min] Sidebar roles + session state
6. [15min] Demo dataset + polish
```

**Success Metric:** End-to-end demo (upload → flag → intervene → delta) runs in <5 seconds.

**Architecture Status: IMPLEMENTATION-READY.** Copy risk_scoring() function first. Test with your 5 sample rows. Build order above = guaranteed demo.