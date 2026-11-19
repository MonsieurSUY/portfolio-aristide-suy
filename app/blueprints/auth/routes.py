from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user

from app.blueprints.auth import auth_bp
from app.extensions import limiter
from app.forms import LoginForm
from app.models import AdminUser


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    # Local desktop mode: the server only listens on this PC, so skip the password.
    if current_app.config["LOCAL_ADMIN"] and request.remote_addr in ("127.0.0.1", "::1"):
        user = AdminUser.query.first()
        if user:
            login_user(user)
            next_url = request.args.get("next")
            return redirect(next_url if next_url and next_url.startswith("/") else url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Connexion réussie.", "success")
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("admin.dashboard"))
        flash("Identifiant ou mot de passe incorrect.", "error")

    return render_template("admin/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("auth.login"))
