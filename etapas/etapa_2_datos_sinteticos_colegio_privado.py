import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Etapa 2 · Generación de datos sintéticos para el Caso 6
# Responsable: Rafael Eladio Moronta (GitHub: jinfron)
# Semilla fija para reproducibilidad
np.random.seed(42)

n_students_base = 4000
years = [2022, 2023, 2024, 2025]
campuses = ["Santo Domingo", "San Pedro de Macorís", "La Romana"]
grades = [
    "PK", "K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th",
    "8th", "9th", "10th", "11th", "12th"
]

records = []

student_ids = [f"STD_{i:05d}" for i in range(1, n_students_base + 1)]
student_campus = {
    s: np.random.choice(campuses, p=[0.5, 0.25, 0.25]) for s in student_ids
}
student_start_year = {s: np.random.choice(years) for s in student_ids}
student_siblings = {
    s: np.random.choice([0, 1, 2, 3], p=[0.4, 0.4, 0.15, 0.05])
    for s in student_ids
}
student_distance = {
    s: np.round(np.random.gamma(shape=2, scale=3), 2) for s in student_ids
}

for year in years:
    macro_shock = 0.15 if year >= 2024 else 0.0

    for s_id in student_ids:
        if student_start_year[s_id] > year:
            continue

        years_enrolled = year - student_start_year[s_id] + 1
        campus = student_campus[s_id]
        grade = grades[min(years_enrolled - 1, len(grades) - 1)]

        attendance_rate = np.clip(
            np.random.normal(loc=0.92, scale=0.08), 0.50, 1.00
        )
        average_grade = np.clip(
            np.random.normal(loc=82, scale=10), 50, 100
        )
        late_payments = np.random.poisson(lam=1.2)
        outstanding_balance = np.round(
            max(0, np.random.normal(loc=15000 * late_payments, scale=5000)),
            2,
        )
        complaints_last_year = np.random.poisson(lam=0.3)
        scholarship_pct = np.random.choice(
            [0, 10, 25, 50, 75, 100],
            p=[0.6, 0.15, 0.1, 0.08, 0.05, 0.02],
        )

        risk_score = (
            0.30 * (outstanding_balance / 50000)
            + 0.25 * (late_payments / 5)
            + 0.20 * (1 - attendance_rate)
            + 0.15 * ((100 - average_grade) / 50)
            + 0.10 * complaints_last_year
            + macro_shock
            + np.random.normal(0, 0.1)
        )
        base_unenroll_prob = 1 / (1 + np.exp(-risk_score))

        retention_call = int(
            risk_score > 0.4 or outstanding_balance > 20000
        )
        payment_plan_offered = int(
            retention_call == 1 and outstanding_balance > 10000
        )

        adjusted_unenroll_prob = base_unenroll_prob
        if retention_call == 1:
            adjusted_unenroll_prob -= 0.15
        if payment_plan_offered == 1:
            adjusted_unenroll_prob -= 0.20
        adjusted_unenroll_prob = np.clip(
            adjusted_unenroll_prob, 0.01, 0.99
        )

        reenrolled_next_year = int(
            not (np.random.rand() < adjusted_unenroll_prob)
        )

        if reenrolled_next_year == 0:
            withdrawal_form_date = (
                datetime(year, 5, 1)
                + timedelta(days=int(np.random.randint(1, 60)))
            ).strftime("%Y-%m-%d")
            new_school_reported = np.random.choice(
                ["Colegio B", "Colegio C", "Desconocido"],
                p=[0.4, 0.3, 0.3],
            )
            final_enrollment_status = "RETIRADO"
            final_balance_settlement = np.random.choice(
                ["PAGADO", "EN_COBRO_JUDICIAL"], p=[0.7, 0.3]
            )
        else:
            withdrawal_form_date = np.nan
            new_school_reported = np.nan
            final_enrollment_status = "MATRICULADO"
            final_balance_settlement = "AL_DIA"

        if np.random.rand() < 0.05:
            attendance_rate = np.nan
        if np.random.rand() < 0.03:
            average_grade = np.nan

        records.append(
            {
                "academic_year": year,
                "student_id": s_id,
                "campus_id": campus,
                "grade_level": grade,
                "years_enrolled": years_enrolled,
                "attendance_rate": attendance_rate,
                "average_grade": average_grade,
                "late_payments": late_payments,
                "outstanding_balance": outstanding_balance,
                "siblings_enrolled": student_siblings[s_id],
                "family_distance_km": student_distance[s_id],
                "complaints_last_year": complaints_last_year,
                "scholarship_pct": scholarship_pct,
                "retention_call": retention_call,
                "payment_plan_offered": payment_plan_offered,
                "reenrolled_next_year": reenrolled_next_year,
                "withdrawal_form_date": withdrawal_form_date,
                "new_school_reported": new_school_reported,
                "final_enrollment_status": final_enrollment_status,
                "final_balance_settlement": final_balance_settlement,
            }
        )

df = pd.DataFrame(records)

print(
    f"Dataset generado: {len(df):,} observaciones | "
    f"{df['student_id'].nunique():,} estudiantes | "
    f"{df.shape[1]} columnas"
)
print(df["academic_year"].value_counts().sort_index())
print(df[["attendance_rate", "average_grade"]].isna().sum())

df.to_csv("colegio_renovacion_matricula.csv", index=False)
