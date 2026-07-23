"""SQLAlchemy models.

Every translatable text field is stored twice (``_fr`` / ``_en`` suffix).
The plain-named property (e.g. ``project.title``) resolves to the field
matching the current request language, falling back to French.
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.i18n import get_locale


def _localized(instance, field_base):
    """Return instance.<field_base>_<lang>, falling back to the French value."""
    lang = get_locale()
    value = getattr(instance, f"{field_base}_{lang}", None)
    if value:
        return value
    return getattr(instance, f"{field_base}_fr", "")


class Profile(db.Model):
    """Singleton row holding the hero/about content and contact links."""

    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False, default="")
    title_fr = db.Column(db.String(160), default="")
    title_en = db.Column(db.String(160), default="")
    tagline_fr = db.Column(db.String(280), default="")
    tagline_en = db.Column(db.String(280), default="")
    about_fr = db.Column(db.Text, default="")
    about_en = db.Column(db.Text, default="")

    availability_fr = db.Column(db.String(80), default="Disponible")
    availability_en = db.Column(db.String(80), default="Available")

    avatar_filename = db.Column(db.String(255))
    cv_filename = db.Column(db.String(255))

    email = db.Column(db.String(120), default="")
    linkedin_url = db.Column(db.String(255), default="")
    github_url = db.Column(db.String(255), default="")
    phone = db.Column(db.String(40), default="")

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def title(self):
        return _localized(self, "title")

    @property
    def tagline(self):
        return _localized(self, "tagline")

    @property
    def about(self):
        return _localized(self, "about")

    @property
    def availability(self):
        return _localized(self, "availability")


class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    category_fr = db.Column(db.String(80), nullable=False)
    category_en = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(20))  # debutant | confirme | expert | None
    order = db.Column(db.Integer, default=0)

    @property
    def name(self):
        return _localized(self, "name")

    @property
    def category(self):
        return _localized(self, "category")


class Experience(db.Model):
    __tablename__ = "experience"

    id = db.Column(db.Integer, primary_key=True)
    role_fr = db.Column(db.String(160), nullable=False)
    role_en = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(160), nullable=False)
    location = db.Column(db.String(160), default="")
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # None => "en cours" / "present"
    description_fr = db.Column(db.Text, default="")
    description_en = db.Column(db.Text, default="")
    achievements_fr = db.Column(db.Text, default="")  # one bullet per line
    achievements_en = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)

    @property
    def role(self):
        return _localized(self, "role")

    @property
    def description(self):
        return _localized(self, "description")

    @property
    def achievements(self):
        raw = _localized(self, "achievements")
        return [line.strip() for line in raw.splitlines() if line.strip()]


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title_fr = db.Column(db.String(160), nullable=False)
    title_en = db.Column(db.String(160), nullable=False)
    short_description_fr = db.Column(db.String(280), default="")
    short_description_en = db.Column(db.String(280), default="")
    long_description_fr = db.Column(db.Text, default="")
    long_description_en = db.Column(db.Text, default="")
    image_filename = db.Column(db.String(255))
    tech_stack = db.Column(db.String(255), default="")  # comma separated
    demo_url = db.Column(db.String(255), default="")
    source_url = db.Column(db.String(255), default="")
    project_date = db.Column(db.Date, nullable=True)
    order = db.Column(db.Integer, default=0)

    @property
    def title(self):
        return _localized(self, "title")

    @property
    def short_description(self):
        return _localized(self, "short_description")

    @property
    def long_description(self):
        return _localized(self, "long_description")

    @property
    def technologies(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(160), nullable=False)
    degree_fr = db.Column(db.String(200), nullable=False)
    degree_en = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(20), default="")
    verification_url = db.Column(db.String(255), default="")
    # diplome (degree-granting) | certification | formation (short training attended)
    category = db.Column(db.String(20), nullable=False, default="diplome")
    order = db.Column(db.Integer, default=0)

    @property
    def degree(self):
        return _localized(self, "degree")


class Testimonial(db.Model):
    __tablename__ = "testimonial"

    id = db.Column(db.Integer, primary_key=True)
    quote_fr = db.Column(db.Text, nullable=False)
    quote_en = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(120), nullable=False)
    author_role = db.Column(db.String(120), default="")
    author_company = db.Column(db.String(120), default="")
    published = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    @property
    def quote(self):
        return _localized(self, "quote")


class Interest(db.Model):
    __tablename__ = "interest"

    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10), default="✨")  # emoji, edited from admin
    order = db.Column(db.Integer, default=0)

    @property
    def name(self):
        return _localized(self, "name")


class BlogPost(db.Model):
    __tablename__ = "blog_post"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    title_fr = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    excerpt_fr = db.Column(db.String(320), default="")
    excerpt_en = db.Column(db.String(320), default="")
    content_fr = db.Column(db.Text, default="")  # markdown
    content_en = db.Column(db.Text, default="")  # markdown
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def title(self):
        return _localized(self, "title")

    @property
    def excerpt(self):
        return _localized(self, "excerpt")

    @property
    def content(self):
        return _localized(self, "content")


class ContactMessage(db.Model):
    __tablename__ = "contact_message"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), default="")
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
