from app.models.db import Employee

def get_employee_data(employee_id, query):
    emp = Employee.query.get(employee_id)
    if not emp:
        return "Employee not found."

    q = query.lower()
    if "vacation" in q or "sick" in q or "leave" in q:
        return (f"Vacation: {emp.vacation_leave} days, "
                f"Sick: {emp.sick_leave} days.")
    if "review" in q or "performance" in q:
        return f"Performance review date: {emp.review_date}"
    if "department" in q:
        return f"Department: {emp.department}"
    if "contact" in q or "email" in q:
        return f"Contact: {emp.contact}"
    return "Sorry, I can only answer about leave, review, department, or contact."
