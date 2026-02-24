# AEWIS Hackathon Strategy Document

**Version:** 1.0 (Competition-Ready)  
**Date:** February 24, 2026  
**Goal:** Top 3 placement in EdTech/General hackathon  
**Builder:** Solo, Streamlit MVP  

***

## 1. Final 30-Second Pitch Script

**Exact Words (Memorize, 85 words):**

> "Indian colleges track attendance and quizzes daily through ERPs like Fedena, but here's the gap—no system flags declining students early. Teachers only see problems at exam time.  
>  
> AEWIS is different. Admins upload existing CSV data. Simple rules instantly detect risks—like 15% score drops or low attendance. Teachers get prioritized intervention lists.  
>  
> Watch this: live CSV upload, risks light up, intervention toggle, risk count drops 15%.  
>  
> **Zero integration. Activate your data today.**"

**Delivery:** Problem (10s) → Solution (10s) → Live tease (10s). End on benefit.

***

## 2. 4-Minute Demo Script

**Exact Flow (Practice 5x, timer each step):**

```
[0:00-0:30] PITCH (above)
[0:30] "Let me show you live."

[0:35] UPLOAD → "Here's real student data from a typical engineering college."
       st.file_uploader → Click sample CSV (200 students)
       ✅ "Processed. Found 42 high-risk students instantly."

[1:00] ADMIN DASH → "Admin sees college-wide risks."
       KPI cards: "High Risk: 42 | Subjects: Physics worst"
       Heatmap appears → Point: "Red = crisis subjects"

[1:45] DRILL-DOWN → "Click high-risk filter..."
       Table loads → Scroll → "S101, Math, flagged for 18% decline + 68% attendance."

[2:15] TEACHER VIEW → "Switch to teacher role."
       Sidebar click → "Ms. Sharma sees *her* at-risk students only."
       List: S101, S104 → "One-click intervention toggle."

[2:45] IMPACT → "Mark intervention complete..."
       Toggle 3 students → Rerun → "High risks now 36. Down 15%. Impact measured."

[3:15] JUDGE INVITE → "Want to try your own data?"
       "Drag any CSV—works with Fedena exports instantly."

[3:45] CLOSE → "AEWIS sits on top of ERPs. No migration. Early flags save semesters."
```

**Total: 4:00 sharp. Practice 10x.**

***

## 3. Judge Psychology Insights

| Judge Type | What They Care About | AEWIS Win Strategy |
|------------|---------------------|-------------------|
| **Academic** | Real classroom impact | "Flags *before* exam eligibility crisis" |
| **Technical** | Clean code + real-time | Live CSV → instant charts (no mock data) |
| **Business** | Adoption feasibility | "CSV upload = zero integration cost" |
| **Designer** | Visual clarity | Heatmap + KPI cards = instant read |

**Hackathon Truth:** Judges remember *live demos that work*. 80% elimination = crashes/static slides.

***

## 4. What Creates Strong Impression

**Top 5 Impact Moves:**
1. **Judge CSV Upload** - "Try your college data live!" (Personalization win)
2. **Live Metric Delta** - Toggle → "Risks dropped from 42 to 36" (ROI proof)
3. **Heatmap Wow** - Physics lights red → "Class-wide crisis spotted instantly"
4. **Role Switch** - Sidebar click → filtered view (multi-user feels real)
5. **Problem First** - 15s pain before features (not feature vomit)

**Physics Demo Line:** *"Red physics cluster? Entire batch failing—HODs miss this manually."*

***

## 5. Common Mistakes to Avoid

| ❌ Pitfall | ❌ Example | ✅ AEWIS Fix |
|-----------|-----------|-------------|
| **Premature Demo** | Start coding before upload works | Test end-to-end first |
| **AI Hype** | "ML-powered risk prediction" | "Simple rules > blackbox AI" |
| **Scale Lie** | "Handles 100k students" | "Perfect for 5k-student colleges" |
| **No Backup** | Laptop dies → panic | Video + screenshots ready |
| **Too Technical** | Pandas vectorization details | "Upload → instant insights" |
| **No Problem** | Jump to features | 15s pain story first |

**Deadly Sin:** Static screenshots. Live CSV upload = make-or-break.

***

## 6. Backup Demo Plan

**If Live Demo Fails (30% chance):**

```
OPTION A: Pre-recorded Video (2min)
├── 1080p screen capture (full flow)
├── Voiceover matches pitch script
├── File: aewis_demo.mp4 (Google Drive link)

OPTION B: Screenshot Deck (90s fallback)
├── Slide 1: Problem + CSV sample
├── Slide 2: Admin dashboard (annotated)
├── Slide 3: Teacher view + delta
├── Slide 4: "Try it live: [streamlit.app link]"

OPTION C: Phone Demo
├── Deploy to Streamlit Cloud pre-judging
├── QR code on final slide
```

**Pre-Judging:** Deploy to cloud → test link 3x → give judges QR.

***

## 7. Submission Checklist

```
□ [ ] app.py <300 lines, runs locally
□ [ ] Sample CSV (200 rows) auto-loads
□ [ ] End-to-end works: upload → flag → toggle → delta
□ [ ] Deployed to Streamlit Cloud (public URL)
□ [ ] 30s pitch memorized
□ [ ] 4min demo timed (<4:15)
□ [ ] Video backup recorded
□ [ ] Screenshot deck ready
□ [ ] QR code with live link
□ [ ] Edge cases tested (your S101→S105)
□ [ ] "Try my CSV" line practiced
```

**Final Check:** Can stranger upload CSV → see risks in 30 seconds? No → fix.

***

## 8. How to Answer Tough Questions

| Tough Question | Winning Answer |
|----------------|----------------|
| **"Why not just use Fedena reports?"** | "Fedena shows *what happened*. AEWIS flags *what will happen*—15% drops before exam time." |
| **"Isn't this just a dashboard?"** | "Dashboards show data. We track flag → intervention → outcome. That's workflow." |
| **"How's adoption different from other EdTech?"** | "Zero integration. CSV export from *any* ERP works day one." |
| **"What about false positives?"** | "Triple override rules + teacher validation. Show you S106—perfect scores, flagged only for attendance." |
| **"Scale to 50k students?"** | "Pandas handles 10k instantly. Post-hackathon: Postgres + Dask." |
| **"Real validation?"** | "Pilot-ready. Faculty contact testing 100 students next week." |

**Golden Rule:** Never BS. Pivot to demo: *"Let me show you live..."*

***

## Competitive Edge Summary

```
STRENGTHS: Live CSV • Heatmap Wow • Role Switch • Metric Delta • Zero Integration
WEAKNESS: Solo Polish → Counter with flawless execution

90% WIN FACTOR: Demo runs perfectly for every judge.
```

**Status: COMPETITION-READY.** Deploy now. Practice 10x. Film backup. Win this.