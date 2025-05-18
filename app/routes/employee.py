from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.services.nlp_service import get_employee_data

employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/chat", methods=["GET", "POST"])
def chat():
    # Ensure only employees can access
    if session.get("role") != "employee":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        data = request.get_json()
        query = data.get("query", "")
        response = get_employee_data(session["user_id"], query)
        return jsonify({"response": response})

    # GET: render chat page
    return render_template("chat.html")
