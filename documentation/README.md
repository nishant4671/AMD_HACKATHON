# Academic Early Warning & Intervention System (AEWIS)

[
[
[

**AEWIS instantly flags at-risk college students from existing CSV data (attendance + quizzes). Admins see college-wide risks via heatmaps. Teachers get prioritized intervention lists. Zero ERP integration required.**

> **Live Demo:** [streamlit.io link placeholder]  
> **Demo Video:** [YouTube link placeholder]

***

## 🎯 Problem Statement

**Indian colleges collect attendance and quiz data daily** via ERPs like Fedena or Excel sheets, but:

- ❌ **No early warning system** - Risks surface only near exam eligibility
- ❌ **Manual trend spotting** - HODs scan 1000+ rows by hand  
- ❌ **Fragmented signals** - Low attendance OR declining scores missed
- ❌ **No intervention tracking** - Flags exist but no action loop

**Result:** 50-70% of intervention opportunities lost, spiking semester failures.

***

## 💡 Solution

**AEWIS = Intelligence layer atop ANY college data system:**

```
CSV Upload → Risk Engine → Actionable Dashboards → Intervention Tracking
```

**3 Core Rules (explainable, no AI):**
- Attendance < 75% → **FLAGGED**
- Score decline ≥ 15% (Quiz1→Quiz3) → **FLAGGED** 
- Subject average < 40% → **FLAGGED**

***

## 🚀 Features (Hackathon MVP)

- ✅ **CSV Upload** - Works with Fedena exports, Excel, any format
- ✅ **Risk Scoring** - Per-subject flags with clear explanations
- ✅ **Admin Dashboard** - Heatmaps reveal crisis subjects
- ✅ **Teacher Dashboard** - Prioritized intervention lists
- ✅ **Live Impact** - Toggle interventions → watch risk counts drop
- ✅ **Zero Setup** - Deploy in 2 minutes

***

## 🛠 Tech Stack

```
Frontend: Streamlit (Python) + Plotly
Backend: Pandas (vectorized risk engine)
Deployment: Streamlit Cloud (free)
Data: CSV only (no database)
Total: Single app.py (250 lines)
```

***

## 🏃‍♂️ Quick Start (Local)

```bash
# 1. Clone & install
git clone https://github.com/yourusername/aewis.git
cd aewis
pip install -r requirements.txt

# 2. Run
streamlit run app.py
```

**Open:** `http://localhost:8501`

**Demo CSV auto-loads** - No data prep needed!

***

## 🎬 Demo Flow (4 Minutes)

```
1. UPLOAD CSV (200 students) → "✅ 42 high risks found"
2. ADMIN DASH → Physics heatmap turns RED 
3. FILTER high-risk → "S101: 18% decline + 68% attendance"
4. TEACHER VIEW → Ms.Sharma's 8 at-risk students
5. TOGGLE interventions → "Risks: 42 → 36"  
6. "Try YOUR CSV → Instant insights"
```

***

## 📁 File Structure

```
aewis/
├── app.py                 # Complete Streamlit app (250 lines)
├── demo_data.csv          # 200 student sample dataset
├── requirements.txt       # streamlit pandas plotly numpy
├── tests/                 # Edge case CSVs (7 scenarios)
│   ├── tc_perfect.csv
│   ├── tc_decline.csv
│   └── tc_override.csv
├── README.md             # This file
└── docs/                 # Generated docs
    ├── product-spec.md
    └── risk-engine.md
```

***

## 📸 Screenshots

### Admin Dashboard (Risk Heatmap)


### Teacher Intervention List  


### Live Risk Reduction


> **Note:** Screenshots auto-generate post-deploy. Add to `screenshots/` folder.

***

## 🎯 How It Works (Risk Engine)

**Per-subject logic (vectorized Pandas):**

```python
# Flags ANY of:
df['score_drop'] = (df['Quiz1'] - df['Quiz3']) / df['Quiz1'] * 100 >= 15
df['low_attend'] = df['Attendance'] < 75
df['low_avg'] = df[['Quiz1','Quiz2','Quiz3']].mean(axis=1) < 40

# Override safety:
df['override_safe'] = (df['Attendance'] >= 85) & (df['avg_score'] >= 70)
```

**Demo edge cases:**
- Perfect scores + low attendance → **FLAGGED** (eligibility risk)
- Stable low performer → **FLAGGED** (chronic failure)  
- High attendance + scores → **Low** (override wins)

***

## 🛤️ Post-Hackathon Roadmap

```
Phase 1 (Week 1): SQLite persistence + 3 pilots
Phase 2 (Month 3): Fedena API + ₹500/student pricing 
Phase 3 (Month 6): ML dropout prediction
Phase 4 (Month 12): Multi-tenant SaaS ($50k ARR)
```

***

## 🔌 Try It Now

1. **Live Demo:** [streamlit.io/your-app] (coming soon)
2. **Your CSV:** Drag any attendance/quiz export
3. **Deploy:** `streamlit hello` → replace with app.py

**Works with:** Fedena, Excel, Google Sheets, custom ERPs.

***

## 📄 License

```
MIT License - Free for hackathons, pilots, production use.
See LICENSE file for details.
```

***

## 🙌 Acknowledgments

Built for [Hackathon Name] 2026  
**Solo developer** | **4-hour MVP** | **Zero external dependencies**

```
⭐ Star if demo impressed you
🐛 Issues welcome (CSV edge cases especially)
🚀 Contributions: Add ERP connectors!
```

***

**AEWIS: Activate your existing data. Flag risks before they become failures.**