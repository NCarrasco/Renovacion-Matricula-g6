# Etapa 3 · Auditoría y clasificación de variables

**Responsable:** Rafael Eladio Moronta  
**GitHub:** `jinfron`  
**Caso:** Riesgo de no renovación de matrícula — Red Educativa Futuro

## Pregunta guía

> ¿Esta variable existiría, con el mismo valor y significado, al momento de decidir qué familias contactar antes de la campaña de reinscripción?

## Clasificación

| Variable | Clasificación | ¿Disponible al decidir? | Tratamiento |
|---|---|---:|---|
| `student_id` | Identificador | Sí | Excluir de las predictoras |
| `academic_year` | Identificador temporal | Sí | Usar para partición temporal, no como predictor |
| `campus_id` | Predictora válida | Sí | Incluir |
| `grade_level` | Predictora válida | Sí | Incluir |
| `years_enrolled` | Predictora válida | Sí | Incluir |
| `attendance_rate` | Predictora válida | Sí | Incluir; imputar faltantes con mediana |
| `average_grade` | Predictora válida | Sí | Incluir; imputar faltantes con mediana |
| `late_payments` | Predictora válida | Sí | Incluir |
| `outstanding_balance` | Predictora válida | Sí | Incluir |
| `siblings_enrolled` | Predictora válida | Sí | Incluir |
| `family_distance_km` | Predictora válida | Sí | Incluir |
| `complaints_last_year` | Predictora válida | Sí | Incluir |
| `scholarship_pct` | Predictora válida | Sí | Incluir |
| `retention_call` | Intervención | No, ocurre después de priorizar | Excluir de las predictoras |
| `payment_plan_offered` | Intervención | No, ocurre después de priorizar | Excluir de las predictoras |
| `reenrolled_next_year` | Target | No | Usar solo como variable objetivo |
| `withdrawal_form_date` | Fuga de información | No | Excluir |
| `new_school_reported` | Fuga de información | No | Excluir |
| `final_enrollment_status` | Fuga de información | No | Excluir |
| `final_balance_settlement` | Fuga de información | No | Excluir |

## Variables predictoras definitivas

```text
campus_id
grade_level
years_enrolled
attendance_rate
average_grade
late_payments
outstanding_balance
siblings_enrolled
family_distance_km
complaints_last_year
scholarship_pct
```

## Variables excluidas

- Identificadores: `student_id`, `academic_year`.
- Intervenciones: `retention_call`, `payment_plan_offered`.
- Fuga posterior: `withdrawal_form_date`, `new_school_reported`, `final_enrollment_status`, `final_balance_settlement`.
- Target: `reenrolled_next_year`.

## Riesgo metodológico controlado

Las variables de intervención y fuga no deben entrar al modelo porque permitirían usar información generada después de la decisión. Esto produciría *data leakage* y un desempeño artificialmente alto que no podría reproducirse en producción.

## Limitación identificada

El caso habla de priorizar 300 familias, pero el dataset utiliza `student_id` y no contiene `family_id`. Por tanto, el procedimiento realmente prioriza estudiantes. Esta diferencia debe declararse como una limitación de la simulación.
