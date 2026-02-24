# Academic Early Warning & Intervention System (AEWIS)  
## Product Definition Document (PDD)

**Version:** 1.0 (Hackathon MVP)  
**Date:** February 24, 2026  
**Author:** Solo Builder  
**Tech Stack:** Streamlit + Python + Pandas + Plotly  

***

## 1. Problem Statement

**Real-World Context:**  
Mid-sized Indian private colleges (1,500–5,000 students) collect attendance and quiz scores daily via ERPs (Fedena) or Excel. Data exists but serves only record-keeping—admins and teachers manually scan for performance declines, flagging at-risk students only near exam eligibility deadlines. Result: 50-70% of intervention opportunities missed, leading to higher failure rates and dropouts. Current workflows are reactive: risks surface too late for meaningful support.

**Quantified Pain:** Late detection means teachers intervene post-decline rather than preventing it.

***

## 2. Why Current ERP Systems Fail at Early Detection

- **Fedena:** Attendance tracking + reports; no automated decline detection or risk scoring.
- **Frappe Education:** Grade entry + basic analytics; no trend-based flagging or intervention workflows.
- **Excel/Custom Sheets:** Manual calculations; no real-time insights or teacher action tracking.
- **Core Gap:** ERPs digitize data collection but lack intelligence layer—passive storage, not proactive alerts.

***

## 3. Target Users and Stakeholders

| Role | Responsibilities | Pain Point |
|------|------------------|------------|
| **Admin/HOD** | Upload data, monitor risks college-wide | Manual trend spotting across 1000+ students |
| **Teacher** | View assigned at-risk students, mark interventions | Late notifications, no clear action tracking |
| **College Principal** (Buyer) | Approve adoption, measure outcomes | Lack of data-driven academic performance visibility |

**Primary Buyer:** Academic HODs in mid-sized private engineering/commerce colleges (Pune/Maharashtra focus).

***

## 4. Core Value Proposition

**AEWIS turns siloed ERP/Excel data into instant, explainable risk alerts + intervention tracking.**  
- **Upload CSV → Auto-flag declines → Teacher action → Measure impact.**  
- **Differentiation:** Rule-based early warning (not AI), zero integration, works atop any system.  
- **Outcome:** Catch 20% more at-risk students early via simple 15% score drop + low attendance rules.

***

## 5. MVP Feature List (Strictly Minimal - 4-6 Hour Build)

**Core Workflow (End-to-End):**
1. **CSV Upload** - Admin uploads structured file (StudentID,Subject,Quiz1-3,Attendance).
2. **Risk Scoring Engine** - Per-subject flags: ANY of (attend<75%, drop≥15% Quiz1→3, avg<40%).
3. **Admin Dashboard** - Risk count pie chart, subject heatmap, high-risk table w/ reasons.
4. **Teacher Dashboard** - Filtered risk list + "Intervene" toggle (updates status).
5. **Demo Simulation** - Toggle intervention → show "risks down 15%" delta.

**Technical Deliverables:**
```
- Single Streamlit app.py (200 lines max)
- Pandas risk function (vectorized <100ms)
- Plotly heatmap + KPI cards
- Session state for role switching
```

***

## 6. Explicit Non-Goals (Scope Lock)

| ❌ CUT FROM MVP | Reason |
|----------------|--------|
| Student dashboard/role | Low demo value, doubles UI effort |
| Teacher matching algorithm | Complex; risks core focus |
| Resource management (labs/sports) | Unrelated scope creep |
| API integrations | Hackathon impossible |
| Email/SMS notifications | External dependencies |
| User authentication (real) | Demo hardcoded roles |
| Data persistence (DB) | In-memory only |
| Predictive ML | Rule-based wins hackathons |
| Export reports | Add if time; not core |

***

## 7. One-Line Pitch

**"CSV → Risk Flags → Teacher Action: Early warning intelligence layer for any college ERP."**

***

## 8. 30-Second Pitch Version

"Colleges collect attendance and quiz data daily, but ERPs like Fedena just store it—no early warnings. Students slip through until exam time. AEWIS is a lightweight Python app: admins upload CSV files, it instantly flags at-risk students using transparent rules—like 15% score drops or low attendance—then teachers see personalized intervention lists. Watch: upload data, see risks light up, toggle action, risks drop 15%. Proactive academic intelligence, zero integration needed."

***

## 9. Product Positioning

| **AEWIS** | **vs ERP Replacement** | **vs Generic Dashboard** |
|-----------|------------------------|-------------------------|
| **Intelligence Layer** | Works *atop* Fedena/Frappe | **Education-Specific Rules** |
| CSV upload (5 sec) | No rip-and-replace | Pre-built decline detection |
| ₹0 setup | Low adoption friction | Intervention workflow baked-in |

**Tagline:** *"Activate your existing data. No migration required."*

***

## 10. Clear Scope Boundaries

```
🎯 IN SCOPE (MVP):                    ❌ OUT OF SCOPE:
- CSV → Risk → Dashboard → Action    - Real database
- Admin + Teacher views              - Multi-college tenancy  
- Explainable rules (3 signals)      - Mobile/responsive design
- Live demo simulation               - Advanced visualizations
- 200-student dataset                - Long-term analytics
```

**Success Metric:** 5-minute demo runs flawlessly; judges upload their CSV → see personalized risks.

***

**Status: BUILD-READY**  
**Demo Data:** Generate 200-row synthetic CSV (50% declines, 20% attendance risks).  
**Next Step:** Code risk engine first → test edges → build dashboards.  

**Document Complete.** Scope locked. Execute.