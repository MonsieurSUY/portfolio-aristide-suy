import re
from datetime import date

from flask import (
    render_template, redirect, url_for, flash, request, session,
    Response, send_from_directory, current_app, abort,
)

from app.blueprints.public import public_bp
from app.extensions import db
from app.forms import ContactForm
from app.i18n import t
from app.models import (
    Profile, Skill, Experience, Project, Education, Testimonial, Interest,
    BlogPost, ContactMessage,
)


def _skills_by_category():
    skills = Skill.query.order_by(Skill.order.asc(), Skill.id.asc()).all()
    grouped = {}
    for skill in skills:
        grouped.setdefault(skill.category, []).append(skill)
    return grouped


def _education_by_category():
    items = Education.query.order_by(Education.order.asc(), Education.id.asc()).all()
    grouped = {"diplome": [], "certification": [], "formation": []}
    for item in items:
        grouped.setdefault(item.category, []).append(item)
    return grouped


def _tools():
    """Software/tool names for the marquee, split from the 'Informatique' skills."""
    tools = []
    for skill in Skill.query.filter_by(category_fr="Informatique").order_by(Skill.order.asc()).all():
        tools += [part.strip() for part in re.split(r"[,;]", skill.name) if part.strip()]
    return tools


@public_bp.route("/", methods=["GET"])
def index():
    profile = Profile.query.first()
    contact_form = ContactForm()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    education_by_category = _education_by_category()
    skills_by_category = _skills_by_category()
    tools = _tools()

    stats = []
    if experiences:
        years = int((date.today() - min(e.start_date for e in experiences)).days / 365.25)
        if years >= 1:
            stats.append((years, "stats.years", "+"))
        stats.append((len(experiences), "stats.experiences", ""))
    trainings = sum(len(v) for v in education_by_category.values())
    if trainings:
        stats.append((trainings, "stats.trainings", ""))
    if tools:
        stats.append((len(tools), "stats.tools", ""))

    context = dict(
        profile=profile,
        skills_by_category=skills_by_category,
        hero_chips=list(skills_by_category.keys())[:3],
        tools=tools,
        stats=stats,
        experiences=experiences,
        projects=Project.query.order_by(Project.order.asc(), Project.id.asc()).all(),
        education_by_category=education_by_category,
        testimonials=Testimonial.query.filter_by(published=True).order_by(Testimonial.order.asc()).all(),
        interests=Interest.query.order_by(Interest.order.asc(), Interest.id.asc()).all(),
        blog_posts=BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all(),
        contact_form=contact_form,
    )
    return render_template("public/index.html", **context)


@public_bp.route("/contact", methods=["POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            subject=(form.subject.data or "").strip(),
            message=form.message.data.strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash(t("contact.success"), "success")
    else:
        flash(t("contact.error"), "error")
    return redirect(url_for("public.index", _anchor="contact"))


@public_bp.route("/blog/<slug>")
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    profile = Profile.query.first()
    return render_template("public/blog_post.html", post=post, profile=profile)


@public_bp.route("/cv")
def download_cv():
    profile = Profile.query.first()
    if not profile or not profile.cv_filename:
        abort(404)
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], profile.cv_filename, as_attachment=True,
        download_name=f"CV-{profile.full_name.replace(' ', '-')}.pdf",
    )


@public_bp.route("/set-language/<lang>")
def set_language(lang):
    if lang in current_app.config["LANGUAGES"]:
        session["lang"] = lang
    next_url = request.referrer or url_for("public.index")
    return redirect(next_url)


@public_bp.route("/favicon.ico")
def favicon_ico():
    return redirect(url_for("static", filename="img/favicon.svg"))


@public_bp.route("/robots.txt")
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {current_app.config['SITE_URL']}/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@public_bp.route("/sitemap.xml")
def sitemap_xml():
    base = current_app.config["SITE_URL"].rstrip("/")
    urls = [f"{base}{url_for('public.index')}"]
    for post in BlogPost.query.filter_by(published=True).all():
        urls.append(f"{base}{url_for('public.blog_post', slug=post.slug)}")

    xml_items = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xml_items}</urlset>'
    return Response(xml, mimetype="application/xml")
