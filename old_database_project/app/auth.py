from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, current_user

auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates", static_folder="static", static_url_path="/auth/static")


@auth_bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))

    return render_template("auth/login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth_bp.login"))

    login_user(user, remember=True)
    return redirect(url_for("main_bp.home"))


@auth_bp.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))
        
    return render_template("auth/register.html")


@auth_bp.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        return redirect(url_for("auth_bp.register"))

    new_user = User(username=username, password=generate_password_hash(
        password, method="sha256"))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth_bp.login"))
