"""Application factory."""
import os

from dotenv import load_dotenv

# Must run before `app.config` is imported: Config's class attributes are
# evaluated at import time via os.environ.get(...), so .env has to be loaded first.
load_dotenv()

import bleach
import markdown as md
from flask import Flask, request, session, g

from app.config import config_by_name
from app.extensions import db, migrate, login_manager, limiter
from app.i18n import get_locale, t, month_year

ALLOWED_MD_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li", "a", "h1", "h2", "h3", "h4",
    "blockquote", "code", "pre", "hr", "img", "span",
]
ALLOWED_MD_ATTRS = {"a": ["href", "title", "rel", "target"], "img": ["src", "alt", "title"]}


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    from app.models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    # ---- Blueprints ----
    from app.blueprints.public import public_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.auth import auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # ---- CLI commands ----
    from app.cli import register_cli

    register_cli(app)

    # ---- i18n ----
    @app.before_request
    def set_language():
        if "lang" not in session:
            session["lang"] = app.config["DEFAULT_LANGUAGE"]
        g.lang = get_locale()

    app.jinja_env.globals["t"] = t
    app.jinja_env.globals["month_year"] = month_year

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from flask import url_for

        lang = get_locale()
        static_export = app.config.get("STATIC_EXPORT", False)
        if static_export:
            # Pre-rendered site: French at "/", English under "/en/".
            prefix = "/en" if lang == "en" else ""
            urls = {
                "home_url": prefix + "/",
                "lang_switch_url": "/" if lang == "en" else "/en/",
                "cv_url": app.config.get("CV_STATIC_URL", "/cv.pdf"),
                "post_url": lambda slug: f"{prefix}/blog/{slug}/",
            }
        else:
            urls = {
                "home_url": url_for("public.index"),
                "lang_switch_url": url_for("public.set_language", lang="en" if lang == "fr" else "fr"),
                "cv_url": url_for("public.download_cv"),
                "post_url": lambda slug: url_for("public.blog_post", slug=slug),
            }
        return {"current_year": datetime.utcnow().year, "static_export": static_export, **urls}

    # ---- Template filters ----
    @app.template_filter("markdown")
    def markdown_filter(text):
        if not text:
            return ""
        html = md.markdown(text, extensions=["extra", "sane_lists"])
        return bleach.clean(html, tags=ALLOWED_MD_TAGS, attributes=ALLOWED_MD_ATTRS, strip=True)

    # ---- Error handlers ----
    from flask import render_template

    @app.errorhandler(404)
    def not_found(e):
        return render_template("public/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("public/500.html"), 500

    return app
