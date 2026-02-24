# AEWIS Data Model and CSV Schema Document

**Version:** 1.0 (Hackathon MVP)  
**Date:** February 24, 2026  
**Format:** Strict 7-column CSV (flat table, no relations)  
**Volume:** Optimized for 200-5,000 student datasets  

***

## 1. Required CSV Fields

| Column | Purpose | Example |
|--------|---------|---------|
| `StudentID` | Unique student identifier | `S101`, `STD2025_001` |
| `Subject` | Course/Subject name | `Mathematics`, `Physics-I` |
| `Quiz1` | First assessment score (0-100) | `72` |
| `Quiz2` | Second assessment score (0-100) | `65` |
| `Quiz3` | Third assessment score (0-100) | `54` |
| `Attendance` | Attendance percentage (0-100) | `68` |

***

## 2. Optional Fields

| Column | Purpose | Default |
|--------|---------|---------|
| `Teacher` | Assigned teacher ID/name | `"Unassigned"` |
| `Class` | Section/Batch identifier | `"A1"`, `"B2"` |
| `Semester` | Academic term | `"2026_S1"` |

***

## 3. Data Type Definitions

```python
CSV → Pandas dtype mapping:
StudentID: str          # S101, STD2025_001
Subject: category       # Math, Physics (20 unique max)
Quiz1,Quiz2,Quiz3: float64  # 85.5, 72.0 (decimal scores)
Attendance: int32       # 68, 92 (whole %)
Teacher: category       # T001, Sharma (50 unique max)
Class: category         # A1, B2 (10 unique max)
```

***

## 4. Entity Relationships

**Flat Denormalized Model (MVP):**
```
StudentID × Subject = Primary Key (composite)
↓ One row per student-subject combination
[ S101 × Math ]
[ S101 × Physics ]
[ S102 × Math ]
```

**Logical Entities:**
```
Student 1:M SubjectPerformance 1:1 RiskScore
   ↓
[Risk flagged per subject, not student]
```

***

## 5. Data Validation Rules

| Rule | Check | Action |
|------|-------|--------|
| **Schema** | Exactly 6+ required columns | `st.error("Missing columns")` |
| **StudentID** | Non-empty string, max 20 chars | Fill `"Unknown"` |
| **Subject** | Non-empty, max 50 chars | Fill `"Unknown_Subject"` |
| **Quiz Scores** | 0 ≤ score ≤ 100 | Clamp to 0-100 |
| **Attendance** | 0 ≤ attend ≤ 100 | Clamp to 0-100 |
| **No Duplicates** | Unique (StudentID,Subject) | Keep first, warn user |

**Pandas Implementation:**
```python
def validate_schema(df):
    required = ['StudentID','Subject','Quiz1','Quiz2','Quiz3','Attendance']
    missing = [col for col in required if col not in df.columns]
    if missing: raise ValueError(f"Missing: {missing}")
    
    # Clamp numeric bounds
    for col in ['Quiz1','Quiz2','Quiz3','Attendance']:
        df[col] = df[col].clip(0, 100)
    
    # Dedupe
    initial_count = len(df)
    df = df.drop_duplicates(subset=['StudentID','Subject'])
    if len(df) < initial_count:
        st.warning(f"Removed {initial_count - len(df)} duplicates")
```

***

## 6. Handling Missing Values

| Column | Strategy | Default |
|--------|----------|---------|
| `StudentID` | Required | `st.error("Missing StudentID")` |
| `Subject` | Required | `st.error("Missing Subject")` |
| `Quiz1,2,3` | Mean of available quizzes | `df['Quiz1'].fillna(df['Quiz1'].mean())` |
| `Attendance` | Subject median | `df.groupby('Subject')['Attendance'].median()` |
| `Teacher` | `"Unassigned"` | Optional field |
| `Class` | `"General"` | Optional field |

**Safe Defaults:**
```python
df['Quiz1'] = df['Quiz1'].fillna(df[['Quiz1','Quiz2','Quiz3']].mean(axis=1))
df['Attendance'] = df['Attendance'].fillna(df.groupby('Subject')['Attendance'].transform('median'))
```

***

## 7. Data Normalization Approach

**Minimal Normalization (Hackathon):**
```
1. Lowercase Subject names → "mathematics", "physics"
2. Standardize StudentID format (strip spaces)
3. Quiz scores to 1 decimal → 85.0, 72.5
4. No further normalization (flat CSV)
```

**Post-Hackathon (v1.1):**
```
Student Dim → Subject Dim → FactPerformance (star schema)
```

***

## 8. Scalability Path for Multi-College

| Phase | Schema Addition | Storage |
|-------|----------------|---------|
| **MVP** | None | Pandas in-memory |
| **Pilot** | `CollegeID` column | SQLite |
| **v1.0** | `CollegeID`, `UploadDate` | Postgres partitioned |
| **SaaS** | Full star schema | Multi-tenant Postgres |

**Multi-College CSV:**
```
CollegeID,StudentID,Subject,Quiz1,Quiz2,Quiz3,Attendance
"PU_001","S101","Math",72,65,54,68
"PU_001","S102","Math",85,88,90,92
"DE_002","S201","Physics",40,38,35,74
```

***

## 9. Example Schema Table

**Valid Demo CSV (10 rows):**
```csv
StudentID,Subject,Quiz1,Quiz2,Quiz3,Attendance,Teacher,Class
S101,Mathematics,72,65,54,68,T001,A1
S102,Mathematics,85,88,90,92,T001,A1
S103,Physics,40,38,35,74,T002,A1
S104,Physics,78,79,77,60,T002,A1
S105,Mathematics,55,50,42,72,T001,A2
S106,Physics,95,96,94,60,T002,A1
S107,Chemistry,38,39,37,80,T003,B1
S108,Mathematics,45,60,75,85,T001,A2
S109,Physics,85,30,88,80,T002,A1
S110,Chemistry,88,87,86,92,T003,B1
```

**Post-Processing Output:**
| StudentID | Subject | Quiz1 | Quiz2 | Quiz3 | Attendance | avg_score | risk_level | risk_reason |
|-----------|---------|-------|-------|-------|------------|-----------|------------|-------------|
| S101 | Mathematics | 72 | 65 | 54 | 68 | 63.7 | High | Decline≥15%, Attendance<75% |
| S102 | Mathematics | 85 | 88 | 90 | 92 | 87.7 | Low | None |

***

## Implementation Code Snippet

```python
def load_and_validate_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    
    # Schema validation
    required_cols = ['StudentID','Subject','Quiz1','Quiz2','Quiz3','Attendance']
    if not all(col in df.columns for col in required_cols):
        st.error("Missing required columns")
        st.stop()
    
    # Data cleaning pipeline
    df = df.drop_duplicates(['StudentID','Subject'])
    numeric_cols = ['Quiz1','Quiz2','Quiz3','Attendance']
    df[numeric_cols] = df[numeric_cols].clip(0, 100)
    
    # Optional columns
    df['Teacher'] = df.get('Teacher', 'Unassigned').fillna('Unassigned')
    df['Class'] = df.get('Class', 'General').fillna('General')
    
    return df
```

**Status: CSV READY.** Generate 200-row sample → test validation → integrate with risk engine. Zero schema ambiguity.