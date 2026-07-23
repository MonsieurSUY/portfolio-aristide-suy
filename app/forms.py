"""Flask-WTF forms for the public site and the admin CRUD screens."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, PasswordField, BooleanField,
    IntegerField, SelectField, DateField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, URL


IMAGE_EXTS = ["png", "jpg", "jpeg", "webp", "gif"]
PDF_EXTS = ["pdf"]


# ---------------------------------------------------------------- Auth ----
class LoginForm(FlaskForm):
    username = StringField("Identifiant", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember = BooleanField("Se souvenir de moi")


# ------------------------------------------------------------- Public -----
class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(max=120)])
    email = StringField(validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField(validators=[Optional(), Length(max=200)])
    message = TextAreaField(validators=[DataRequired(), Length(max=5000)])


# -------------------------------------------------------------- Admin -----
class ProfileForm(FlaskForm):
    full_name = StringField("Nom complet", validators=[DataRequired(), Length(max=120)])
    title_fr = StringField("Titre professionnel (FR)", validators=[DataRequired()])
    title_en = StringField("Titre professionnel (EN)", validators=[DataRequired()])
    tagline_fr = StringField("Phrase d'accroche (FR)", validators=[Optional(), Length(max=280)])
    tagline_en = StringField("Phrase d'accroche (EN)", validators=[Optional(), Length(max=280)])
    about_fr = TextAreaField("À propos (FR, markdown)", validators=[Optional()])
    about_en = TextAreaField("À propos (EN, markdown)", validators=[Optional()])
    availability_fr = SelectField(
        "Disponibilité (FR)",
        choices=[("Disponible", "Disponible"), ("En poste", "En poste"), ("Ouvert aux opportunités", "Ouvert aux opportunités")],
    )
    availability_en = SelectField(
        "Disponibilité (EN)",
        choices=[("Available", "Available"), ("Employed", "Employed"), ("Open to opportunities", "Open to opportunities")],
    )
    email = StringField("Email", validators=[Optional(), Email(), Length(max=120)])
    linkedin_url = StringField("LinkedIn", validators=[Optional(), URL(), Length(max=255)])
    github_url = StringField("GitHub", validators=[Optional(), URL(), Length(max=255)])
    phone = StringField("Téléphone", validators=[Optional(), Length(max=40)])
    avatar = FileField("Photo de profil", validators=[Optional(), FileAllowed(IMAGE_EXTS, "Images uniquement.")])
    cv = FileField("CV (PDF)", validators=[Optional(), FileAllowed(PDF_EXTS, "PDF uniquement.")])


class SkillForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=100)])
    name_en = StringField("Nom (EN)", validators=[DataRequired(), Length(max=100)])
    category_fr = StringField("Catégorie (FR)", validators=[DataRequired(), Length(max=80)])
    category_en = StringField("Catégorie (EN)", validators=[DataRequired(), Length(max=80)])
    level = SelectField(
        "Niveau",
        choices=[("", "—"), ("debutant", "Débutant"), ("confirme", "Confirmé"), ("expert", "Expert")],
        validators=[Optional()],
    )
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class ExperienceForm(FlaskForm):
    role_fr = StringField("Poste (FR)", validators=[DataRequired(), Length(max=160)])
    role_en = StringField("Poste (EN)", validators=[DataRequired(), Length(max=160)])
    company = StringField("Entreprise", validators=[DataRequired(), Length(max=160)])
    location = StringField("Lieu", validators=[Optional(), Length(max=160)])
    start_date = DateField("Date de début", validators=[DataRequired()])
    end_date = DateField("Date de fin (vide = en cours)", validators=[Optional()])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    description_en = TextAreaField("Description (EN)", validators=[Optional()])
    achievements_fr = TextAreaField("Réalisations (FR, une par ligne)", validators=[Optional()])
    achievements_en = TextAreaField("Réalisations (EN, une par ligne)", validators=[Optional()])
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class ProjectForm(FlaskForm):
    title_fr = StringField("Titre (FR)", validators=[DataRequired(), Length(max=160)])
    title_en = StringField("Titre (EN)", validators=[DataRequired(), Length(max=160)])
    short_description_fr = StringField("Description courte (FR)", validators=[Optional(), Length(max=280)])
    short_description_en = StringField("Description courte (EN)", validators=[Optional(), Length(max=280)])
    long_description_fr = TextAreaField("Description longue (FR)", validators=[Optional()])
    long_description_en = TextAreaField("Description longue (EN)", validators=[Optional()])
    image = FileField("Image / capture d'écran", validators=[Optional(), FileAllowed(IMAGE_EXTS, "Images uniquement.")])
    tech_stack = StringField("Technologies (séparées par des virgules)", validators=[Optional(), Length(max=255)])
    demo_url = StringField("Lien démo", validators=[Optional(), URL(), Length(max=255)])
    source_url = StringField("Lien code source", validators=[Optional(), URL(), Length(max=255)])
    project_date = DateField("Date", validators=[Optional()])
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class EducationForm(FlaskForm):
    institution = StringField("Établissement", validators=[DataRequired(), Length(max=160)])
    degree_fr = StringField("Intitulé (FR)", validators=[DataRequired(), Length(max=200)])
    degree_en = StringField("Intitulé (EN)", validators=[DataRequired(), Length(max=200)])
    year = StringField("Année", validators=[Optional(), Length(max=20)])
    verification_url = StringField("Lien de vérification", validators=[Optional(), URL(), Length(max=255)])
    category = SelectField(
        "Type",
        choices=[
            ("diplome", "Diplôme / formation diplômante"),
            ("certification", "Certification"),
            ("formation", "Formation suivie"),
        ],
        validators=[DataRequired()],
    )
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class TestimonialForm(FlaskForm):
    quote_fr = TextAreaField("Citation (FR)", validators=[DataRequired()])
    quote_en = TextAreaField("Citation (EN)", validators=[DataRequired()])
    author_name = StringField("Nom", validators=[DataRequired(), Length(max=120)])
    author_role = StringField("Poste", validators=[Optional(), Length(max=120)])
    author_company = StringField("Entreprise", validators=[Optional(), Length(max=120)])
    published = BooleanField("Publié", default=True)
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class InterestForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=100)])
    name_en = StringField("Nom (EN)", validators=[DataRequired(), Length(max=100)])
    icon = StringField("Icône (emoji)", validators=[Optional(), Length(max=10)])
    order = IntegerField("Ordre", default=0, validators=[Optional()])


class BlogPostForm(FlaskForm):
    slug = StringField("Slug (URL)", validators=[DataRequired(), Length(max=200)])
    title_fr = StringField("Titre (FR)", validators=[DataRequired(), Length(max=200)])
    title_en = StringField("Titre (EN)", validators=[DataRequired(), Length(max=200)])
    excerpt_fr = StringField("Extrait (FR)", validators=[Optional(), Length(max=320)])
    excerpt_en = StringField("Extrait (EN)", validators=[Optional(), Length(max=320)])
    content_fr = TextAreaField("Contenu (FR, markdown)", validators=[Optional()])
    content_en = TextAreaField("Contenu (EN, markdown)", validators=[Optional()])
    published = BooleanField("Publié", default=False)
