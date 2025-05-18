from flask import Blueprint, request, session, jsonify
from flask import render_template, session, redirect, url_for

from app.models.db import Employee

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/view_employee")
def view_employee():
    if session.get("role") != "admin":
        return jsonify({"error":"Admin only"}), 403
    eid = request.args.get("id")
    emp = Employee.query.get(eid)
    if not emp:
        return jsonify({"error":"Not found"}), 404
    return jsonify({
        "id": emp.id,
        "name": emp.name,
        "department": emp.department,
        "contact": emp.contact,
        "vacation_leave": emp.vacation_leave,
        "sick_leave": emp.sick_leave,
        "review_date": emp.review_date
    })

@admin_bp.route('/dashboard')
def dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")


@admin_bp.route("/list_employees")
def list_employees():
    if session.get("role") != "admin":
        return jsonify({"error":"Admin only"}), 403
    emps = Employee.query.all()
    return jsonify([{"id":e.id, "name":e.name} for e in emps])
