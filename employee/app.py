from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from repository.employee_repository import create_employee, get_employee_by_email
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        employee_id = request.form["employee_id"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        department = request.form["department"].strip()

        if not employee_id or not name or not email or not password:
            error = "All fields are required"

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid email format"

        elif len(password) < 6:
            error = "Password must be at least 6 characters"

        else:
            hashed_password = generate_password_hash(password)

            success = create_employee(
                employee_id, name, email, hashed_password, department
            )

            if not success:
                error = "Employee ID or Email already exists"
            else:
                return redirect("/")

    return render_template("register.html", error=error)


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        employee = get_employee_by_email(email)

        if employee and check_password_hash(employee["password"], password):
            session["employee"] = employee["name"]
            return redirect("/dashboard")
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "employee" not in session:
        return redirect("/")
    return render_template("dashboard.html", name=session["employee"])


@app.route("/logout")
def logout():
    session.pop("employee", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)