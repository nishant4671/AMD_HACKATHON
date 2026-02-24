# AEWIS Risks & Limitations Document

**Version:** 1.0 (Brutally Realistic Review)  
**Date:** February 24, 2026  
**Tone:** No sugarcoating. Real-world failure probabilities.  
**Reality:** 90% hackathon projects die. Here's why yours might.

***

## 1. Technical Risks

| Risk | Impact | Mitigation | Harsh Truth |
|------|--------|------------|-------------|
| **Streamlit Rerun Bugs** | Demo crash (50% solos) | Session state discipline | State loss on role switch kills 30% demos |
| **Pandas Memory Spike** | 10k+ rows freeze | Row limit warning | Judges expect "enterprise scale" |
| **Plotly Render Fail** | Blank charts (20%) | `@st.cache_data` | No heatmap = no wow factor |
| **CSV Parse Edge** | `NaN` → `inf` → crash | Bulletproof validation | Indian colleges export garbage CSVs |
| **Deployment Timeout** | Cloud link 404 | Local + cloud both ready | Streamlit Cloud lags under load |

**Killshot:** Laptop battery dies mid-demo → no backup = zero.

***

## 2. Data Quality Risks

| Problem | Prevalence | Demo Impact | Post-Hackathon Reality |
|---------|------------|-------------|----------------------|
| **Inconsistent Schema** | 70% ERP exports | Upload error panic | Every college formats differently |
| **Dirty Scores** | 40% (text in Quiz1) | Silent NaN → wrong flags | Faculty enter "Absent" as scores |
| **Missing Quizzes** | 60% mid-semester | Skewed averages | Quiz2 missing → false declines |
| **Attendance Gaming** | 30% urban colleges | Proxy attendance | 92% attend but failing = wrong lows |
| **Duplicate Students** | 25% transfers | Double-count risks | S101 × 2 → inflated crisis |

**Demo Crutch:** Synthetic data works. Real CSVs crash 70% first tries.

***

## 3. Adoption Risks

| Stakeholder | Objection | Probability | Killer Response Needed |
|-------------|-----------|-------------|----------------------|
| **HODs** | "We use Fedena already" | 85% | "CSV export works with Fedena" |
| **Teachers** | "One more login? No." | 90% | Manual toggle too much friction |
| **Principal** | "What's the ROI?" | 95% | No hard failure reduction stats |
| **IT Admin** | "Security policy violation" | 70% | CSV upload = uncontrolled data |
| **Faculty** | "Students cheat anyway" | 60% | Risk flags don't fix motivation |

**Reality:** 3-month sales cycles. 80% ghost after pilot promise.

***

## 4. False Positive Risks

**Your Rules Sound Good, But...**

| Scenario | Flags Wrong | Business Impact |
|----------|-------------|----------------|
| **Single Bad Quiz** | Quiz2=30, rebounds Quiz3 | Teacher wastes time on good student |
| **Attendance Proxies** | Friend marks present, fails quizzes | Wrong teacher blamed |
| **Gaming Thresholds** | Students hit exactly 75% attend | Rules become known exploits |
| **Subject Difficulty** | New Physics prof, class avg 35% | Entire class flagged |

**Validation Gap:** No real college data = 40% false positives likely.

**Teacher Fatigue:** 50 flags/week → ignored after 2 weeks.

***

## 5. Privacy Concerns

| Issue | Legal Risk (India) | Immediate Problem |
|-------|-------------------|------------------|
| **Student Names** | CSV likely has names | GDPR vibes scare principals |
| **No Consent** | Parents unaware | Ethics committee blocks pilot |
| **CSV Storage** | Session state = memory dump | Data breach if shared hosting |
| **Screenshot Leak** | Demo photos online | FERPA-style complaints |

**Demo Risk:** Judge says "GDPR violation!" → Instant credibility loss.

***

## 6. Scalability Limitations

| Scale | Current Capacity | Failure Mode |
|-------|-------------------|--------------|
| **1 College (5k)** | ✅ Pandas fine | None |
| **10 Colleges** | ❌ No multi-tenancy | CollegeID missing |
| **Real-Time** | ❌ CSV manual | Weekly upload hell |
| **Mobile Faculty** | ❌ Desktop only | Teachers ignore |
| **Historical** | ❌ No trends | Can't prove ROI |

**Post-Hackathon:** Manual CSV = dead product in 3 months.

***

## 7. Hackathon-Specific Risks

| Demo Killer | Probability | Recovery Odds |
|-------------|-------------|---------------|
| **Network Drop** | 40% | Cloud backup MUST work |
| **Judge CSV Bomb** | 60% | Graceful error message |
| **Time Overrun** | 70% | 4:00 hard stop |
| **Polish Gap** | 90% (solo) | Teams win on UI |
| **"So What?"** | 50% academics | Weak problem story |

**Solo Death Spiral:** Bug → recovery → time lost → rushed close → weak finish.

***

## 8. Long-Term Sustainability Challenges

| Year 1 Reality | Probability | Death Cause |
|----------------|-------------|-------------|
| **No Co-Founder** | 95% | Solo burnout |
| **No Paying Pilot** | 85% | Runway ends |
| **ERP Adds Copycat** | 70% | Fedena vNext has "risk flags" |
| **Teacher Non-Adoption** | 90% | Checkbox fatigue |
| **Regulatory Change** | 40% | NEP shifts priorities |

**Market Truth:** EdTech India = 95% failure. Retention tools need district contracts.

***

## Risk Mitigation Priority (Solo Builder)

```
CRITICAL (Fix NOW):
1. [ ] 7 edge case CSVs work perfectly
2. [ ] Cloud + local both flawless
3. [ ] Video backup recorded
4. [ ] 4min timing locked

HIGH (Hackathon survival):
1. [ ] "Try judge CSV" handles garbage
2. [ ] False positive explanation ready
3. [ ] Streamlit Cloud deployed

IGNORE (Post-win):
- Privacy policy
- Multi-tenancy
- Real authentication
```

***

## Brutal Bottom Line

**Hackathon Odds:** 60% demo win if flawless execution  
**Product Odds:** 5% survives 6 months without:  
- Real pilot data  
- Technical co-founder  
- Paying college contract  

**Immediate Threat:** Over-refining docs while coding lags. **Build or die.** Deploy to cloud. Test judge CSV bombs. Practice 10x. Win demo first.

**Status: HIGH RISK.** Every minute reading = lost demo polish. Execute.