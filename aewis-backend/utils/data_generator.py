"""
Generate 512-row synthetic CSV for AEWIS demo.
Columns: student_id, subject, quiz1, quiz2, quiz3, attendance
Physics/Chemistry biased toward decline + low attendance for crisis clustering.
"""
import random
import csv
from pathlib import Path

SUBJECTS = ["Physics", "Chemistry", "Math", "Biology", "English"]
TEACHERS = ["T001_Sharma", "T002_Kumar", "T003_Patel", "T004_Singh", "T005_Mehta"]


def generate_demo_data(num_rows: int = 512) -> list[dict]:
    random.seed(42)
    rows = []
    for i in range(1, num_rows + 1):
        student_id = f"S{i:03d}"
        subject = random.choice(SUBJECTS)
        teacher = random.choice(TEACHERS)
        base = random.randint(35, 85)
        trend = random.gauss(0, 8)
        q1 = max(0, min(100, base))
        q2 = max(0, min(100, base + trend))
        q3 = max(0, min(100, base + trend * 1.5))
        if subject in ("Physics", "Chemistry"):
            q3 = max(0, min(100, q3 - random.randint(5, 20)))
            att = random.gauss(72, 12)
        else:
            att = random.gauss(82, 10)
        attendance = max(0, min(100, att))
        rows.append({
            "student_id": student_id,
            "subject": subject,
            "teacher_id": teacher,
            "quiz1": round(q1, 1),
            "quiz2": round(q2, 1),
            "quiz3": round(q3, 1),
            "attendance": round(attendance, 1),
        })
    return rows


def write_demo_csv(filepath: str | Path, num_rows: int = 512) -> None:
    rows = generate_demo_data(num_rows)
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["student_id", "subject", "teacher_id", "quiz1", "quiz2", "quiz3", "attendance"],
        )
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    write_demo_csv("demo_data.csv", 512)
    print("Generated demo_data.csv with 512 rows")
