# AEWIS Testing & Validation Plan

**Version:** 1.0 (Solo Hackathon QA)  
**Date:** February 24, 2026  
**Goal:** Zero demo crashes, 100% edge case coverage  
**Time Required:** 45 minutes total  

***

## 1. Edge Case Scenarios

**Create these 7 test CSVs (5 rows each):**

| Test Case | Description | Expected Outcome |
|-----------|-------------|-----------------|
| **TC-001: Perfect Student** | Quiz1-3: 95,96,94<br>Attendance: 92% | **Low Risk** (no flags) |
| **TC-002: Decline Only** | Quiz1-3: 85,72,65<br>Attendance: 88% | **High Risk** ("Decline ≥15%") |
| **TC-003: Low Attendance Ace** | Quiz1-3: 92,94,91<br>Attendance: 68% | **High Risk** ("Attendance <75%") |
| **TC-004: Chronic Low** | Quiz1-3: 35,38,36<br>Attendance: 82% | **High Risk** ("Avg <40%") |
| **TC-005: Override Safety** | Quiz1-3: 72,68,75<br>Attendance: 88% | **Low Risk** (override wins) |
| **TC-006: Single Bad Quiz** | Quiz1-3: 88,42,90<br>Attendance: 85% | **Low Risk** (no trend) |
| **TC-007: All Signals** | Quiz1-3: 78,62,48<br>Attendance: 65% | **High Risk** (all 3 flags) |

***

## 2. Data Anomaly Handling

**Test these broken CSVs:**

| Anomaly | Input Example | Expected Behavior |
|---------|---------------|-------------------|
| **Missing Columns** | No `Quiz2` column | `st.error("Missing columns")` → Stop |
| **Wrong Data Types** | `Quiz1 = "abc"` | Coerce to 0 OR clamp 0-100 |
| **Out of Bounds** | `Quiz1 = 150`<br>`Attendance = -5` | Clamp → 100, 0 |
| **Empty Rows** | All NaN row | Skip (dropna) + warning |
| **Duplicates** | S101×Math ×2 | Keep first + "Removed X duplicates" |
| **No Risks** | All perfect scores | "0 high risks" → Green dashboard |

***

## 3. Risk Engine Validation Checklist

**Run each of 5 original samples + verify:**

```
S101: Quiz 72→54 (33% drop), Attend 68% → HIGH "Decline, Attendance"
S102: Quiz 85→90, Attend 92% → LOW "None"  
S103: Quiz 40→35, Attend 74% → HIGH "Avg<40%, Attendance"
S104: Quiz 78→77, Attend 60% → HIGH "Attendance"
S105: Quiz 55→42 (31% drop), Attend 72% → HIGH "Decline, Attendance, Avg"
```

**Formula Check:** `(72-54)/72 * 100 = 25% ≥ 15%` ✓

***

## 4. Manual Test Cases (15min Script)

```
TEST 1: HAPPY PATH [3min]
□ Upload demo CSV → "✅ Loaded 200 records"
□ Admin dashboard → 42 High risks ✓
□ Heatmap shows Physics red ✓
□ Click filter → Table updates ✓

TEST 2: TEACHER ROLE [2min]  
□ Sidebar → Teacher → Ms.Sharma view
□ See 8 at-risk students ✓
□ Toggle 3 → Risk count drops ✓

TEST 3: BROKEN DATA [3min]
□ Upload TC-001 missing column → Error message ✓
□ Upload negative scores → Clamped to 0 ✓
□ Upload 10k dummy rows → <2sec load ✓

TEST 4: VISUALS [2min]
□ Heatmap colors correct (Red=High) ✓
□ KPI cards update on filter ✓
□ No broken charts

TEST 5: JUDGE CSV [2min]
□ Make broken CSV → Upload → Handles gracefully ✓
```

***

## 5. Demo Rehearsal Checklist (10min x 3 runs)

```
TIMED RUN (Target: 4:00 exactly):
□ [0:00] 30s pitch → No "ums"
□ [0:30] CSV upload → Instant success
□ [1:00] Admin dashboard → Point to heatmap
□ [1:45] Filter high-risk → S101 details
□ [2:15] Teacher toggle → "Risks: 42→36"
□ [3:15] "Try your CSV?" → Ready uploader
□ [3:45] Hand QR code

LIVE TEST:
□ Switch WiFi → Still works
□ Close/reopen browser → Session preserved
□ Role switch 3x → No state loss
```

***

## 6. Failure Recovery Strategies

| Failure Mode | Probability | Recovery (10s max) |
|--------------|-------------|-------------------|
| **Upload hangs** | 20% | "Switching to pre-loaded demo data..." |
| **Heatmap blank** | 15% | Screenshot slide → "Live link in bio" |
| **Toggle broken** | 10% | "Here's the before/after numbers..." |
| **Laptop dies** | 5% | Phone → Streamlit Cloud QR |
| **Judge CSV breaks** | 30% | "Perfect—shows real-world validation needed!" |

**Golden Backup:** Streamlit Cloud deployment → QR code always works.

***

## 7. Pre-Submission Sanity Checks (5min Final Sweep)

```
□ [ ] Local: streamlit run app.py → Perfect
□ [ ] Cloud: Deployed + public link works
□ [ ] Demo CSV (200 rows) loads everywhere
□ [ ] All 7 edge CSVs test pass
□ [ ] 4min demo timing <4:15
□ [ ] Video backup recorded (2min)
□ [ ] Screenshot deck ready (6 slides)
□ [ ] QR code tested (opens app)
□ [ ] Pitch memorized (no notes)
□ [ ] "Try my CSV" uploader visible

FINAL SMOKE TEST:
1. Fresh incognito browser
2. Upload demo CSV
3. Admin → Teacher → Toggle → Admin
4. All visuals + interactions work
```

***

## QA Execution Priority (45min Total)

```
Phase 1 (15min): Create 7 edge CSVs → Test risk engine
Phase 2 (15min): Full demo run x3 → Time it
Phase 3 (10min): Broken data tests
Phase 4 (5min):  Sanity checklist → Deploy
```

## Success Criteria

- **Demo runs perfectly** 10/10 times
- **All edge cases handled gracefully** 
- **Judge uploads broken CSV → No crash**
- **Risk counts match expected** (42 High from demo data)

**Status: TESTABLE.** Run Phase 1 now. Fail fast. Fix immediately. Demo or die.

**Post-QA:** You're bulletproof. Submit confidently.