from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import JobApplication
from datetime import datetime

main = Blueprint('main', __name__)

# Home page: show all job applications
@main.route("/")
def index():
    jobs = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
    return render_template("index.html", jobs=jobs)

# Add new job application
@main.route("/add", methods=["GET", "POST"])
def add_job():
    if request.method == "POST":
        company = request.form.get("company")
        position = request.form.get("position")
        status = request.form.get("status")
        date_applied = request.form.get("date_applied")

        if not date_applied:
            date_applied = datetime.utcnow()
        else:
            date_applied = datetime.strptime(date_applied, "%Y-%m-%d")

        new_job = JobApplication(company=company, position=position, status=status, date_applied=date_applied)
        db.session.add(new_job)
        db.session.commit()
        flash("Job application added successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_job.html")

# Edit existing job application
@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_job(id):
    job = JobApplication.query.get_or_404(id)
    if request.method == "POST":
        job.company = request.form.get("company")
        job.position = request.form.get("position")
        job.status = request.form.get("status")
        date_applied = request.form.get("date_applied")
        if date_applied:
            job.date_applied = datetime.strptime(date_applied, "%Y-%m-%d")
        db.session.commit()
        flash("Job application updated successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("edit_job.html", job=job)

# Delete job application
@main.route("/delete/<int:id>", methods=["POST"])
def delete_job(id):
    job = JobApplication.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash("Job application deleted successfully!", "success")
    return redirect(url_for("main.index"))
