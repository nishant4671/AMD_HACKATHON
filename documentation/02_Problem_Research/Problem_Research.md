# AEWIS Problem & Context Research Document

**Version:** 1.0  
**Date:** February 24, 2026  
**Focus:** Mid-sized private Indian colleges (1,500–5,000 students, engineering/commerce)  
**Sources:** ERP docs, adoption analyses, EdTech case patterns [fedena](https://fedena.com/feature-tour/student-attendance-management-system)

***

## 1. Current Academic Workflow in Typical Indian Colleges

**Daily Cycle:**
1. **Morning Roll Call:** Teachers mark attendance manually (registers), via ERP apps (mobile/web), or biometrics (urban colleges).
2. **Weekly Quizzes/Assessments:** Internal tests graded in Excel/ERP; scores entered post-class.
3. **Weekly/Monthly Review:** HOD compiles reports for eligibility checks (e.g., 75% attendance mandate).
4. **Semester-End Crunch:** Bulk analysis for promotions/failures; interventions (tutorials) rushed last 2 weeks.

**Process Flow:** Data entry → Storage → Periodic manual reports → Ad-hoc interventions.

***

## 2. How Attendance and Performance Are Tracked

| Metric | Tools | Frequency | Output |
|--------|-------|-----------|--------|
| **Attendance** | Fedena app/registers/biometrics | Daily | % per subject/class; eligibility alerts (post-facto).  [fedena](https://fedena.com/feature-tour/student-attendance-management-system) |
| **Quizzes/Marks** | Excel sheets/ERP gradebooks | Weekly/monthly | Raw scores; semester averages. |
| **Trends** | Manual Excel pivots (rare) | End-of-month | None automated. |

**Data Flow:** Teacher inputs → Centralized ERP/Sheets → HOD exports for meetings. No real-time aggregation.

***

## 3. Pain Points in Early Intervention

- **Timing Mismatch:** Declines (e.g., Quiz1 80 → Quiz3 50) visible only in bulk reviews; too late for mid-semester fixes.
- **Manual Scanning:** HODs/teachers eyeball 100+ student sheets—no filters for "declining only."
- **Fragmented Signals:** Attendance low but scores ok (or vice versa)—no combined rules.
- **Action Gaps:** Flag spotted → verbal handoff to teacher → no follow-up tracking.
- **Scale Overload:** 200-student classes; manual misses 50% subtle risks.

**Root:** Workflows optimized for compliance (eligibility), not prediction.

***

## 4. Why Data Is Collected but Not Used Proactively

- **Purpose Mismatch:** Data for regulatory compliance (UGC attendance mandates, promotion rules)—not analytics.
- **Tool Limitations:** ERPs report historicals; no forward-looking rules (e.g., "flag 15% drops").
- **Skill Gaps:** Teachers non-technical; admins prioritize admin over analysis.
- **Incentive Void:** No KPIs tied to early interventions; failures blamed on "student effort."
- **Overload Factor:** Daily entry eats time—no bandwidth for weekly scans.

**Outcome:** Data as artifact, not asset.

***

## 5. Limitations of Existing ERPs

| System | Strengths | Early Detection Gaps |
|--------|-----------|----------------------|
| **Fedena**  [fedena](https://fedena.com/feature-tour/student-attendance-management-system) | Biometric attendance, reports. | No performance trends; alerts only for totals <75%. |
| **Frappe Education**  [frappe](https://frappe.io/education) | Grading, student portals. | Basic results views; no decline rules or teacher actions. |
| **LMS (Moodle/Google Classroom)** | Quiz hosting. | Scores isolated; no attendance merge or risk logic. |
| **Custom Excel** | Flexible. | Manual, non-scalable; no dashboards. |

**Common Flaw:** Backward-looking reports vs. forward flags.

***

## 6. Institutional Adoption Constraints

- **Budget:** Mid-tier colleges cap IT at ₹1-5L/year; resist add-ons.
- **Fragmentation:** 40% use hybrid (ERP + Excel); integration aversion. [linkedin](https://www.linkedin.com/pulse/why-most-university-erp-implementations-fail-india-what-anupama-k-zqqgf)
- **Training Resistance:** Faculty 40+ resist new logins/tools.
- **Vendor Lock:** Existing ERP contracts (2-3yr) block switches.
- **Regulatory Focus:** UGC audits favor records over insights.
- **Scale Mismatch:** Tools built for K-12, not college dynamics. [tssreview](https://tssreview.in/wp-content/uploads/2024/05/1-1.pdf)

**Barrier:** Change costs > perceived gains without pilots.

***

## 7. Stakeholder Pain Breakdown

| Stakeholder | Daily Pain | Workflow Friction |
|-------------|------------|------------------|
| **Admin/HOD** | Compiling risks from 10 sheets; late alerts to principal. | Manual exports, no heatmaps. |
| **Teacher** | Owns 80 students; spots issues anecdotally, no prioritized list. | No "at-risk today" view. |
| **Student** | No self-awareness until warnings; misses early help. | Opaque progress. |
| **Principal** | Semester surprises (high failures); lacks defensible metrics. | Reactive meetings. |

**Priority:** HODs bottleneck interventions.

***

## 8. Why Early Warning Systems Are Valuable

- **Proactive Shift:** Flags enable mid-quiz fixes vs. post-exam retakes (global EWS cut dropouts 15-25%). [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10425558/)
- **Resource Efficiency:** Prioritizes top 20% risks over all-students reviews.
- **Accountability:** Tracks "flagged → intervened → outcome," tying actions to results.
- **Low Overhead:** CSV upload = 2min/week vs. daily manual.
- **Scalable Insight:** Heatmaps reveal class-wide issues (e.g., Physics drops).
- **India Fit:** Aligns with NEP 2020 outcome focus without heavy infra.

**Proof Point:** Systems like this layer onto ERPs, activating idle data.

***

**Research Summary:** Problem validated—data abundance, action scarcity. AEWIS fits as minimal layer. Next: Pilot CSV from 1 HOD to quantify flags vs. actual failures. [linkedin](https://www.linkedin.com/pulse/why-most-university-erp-implementations-fail-india-what-anupama-k-zqqgf)