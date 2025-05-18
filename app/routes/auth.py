from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.models.db import User, db

auth_bp = Blueprint("auth", __name__)

# === ✅ Home Page ===
@auth_bp.route('/')
def home():
    return render_template("index.html")

# === ✅ Sign Up ===
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("auth.signup"))

        new_user = User(email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["role"] = new_user.role

        flash("Signed up and logged in!", "success")
        return redirect(
            url_for("employee.chat") if new_user.role == "employee" else url_for("admin.dashboard")
        )

    return render_template("signup.html")

# === ✅ Log In ===
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            flash("Logged in successfully!", "success")
            return redirect(
                url_for("employee.chat") if user.role == "employee" else url_for("admin.dashboard")
            )

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# === ✅ Log Out ===
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))
