from flask import render_template, redirect, url_for, flash, request, abort

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.forms import (
    ProfileForm, SkillForm, ExperienceForm, ProjectForm, EducationForm,
    TestimonialForm, InterestForm, BlogPostForm,
)
from app.models import (
    Profile, Skill, Experience, Project, Education, Testimonial, Interest,
    BlogPost, ContactMessage,
)
from app.utils import save_upload, delete_upload, UploadError


# ---------------------------------------------------------------- Dashboard
@admin_bp.route("/")
def dashboard():
    counts = {
        "skills": Skill.query.count(),
        "experiences": Experience.query.count(),
        "projects": Project.query.count(),
        "education": Education.query.count(),
        "testimonials": Testimonial.query.count(),
        "interests": Interest.query.count(),
        "blog_posts": BlogPost.query.count(),
        "messages": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    return render_template("admin/dashboard.html", counts=counts)


# ------------------------------------------------------------------ Profile
@admin_bp.route("/profile", methods=["GET", "POST"])
def edit_profile():
    profile = Profile.query.first()
    if profile is None:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        form.populate_obj(profile)

        if form.avatar.data:
            try:
                filename = save_upload(form.avatar.data, kind="image")
                delete_upload(profile.avatar_filename)
                profile.avatar_filename = filename
            except UploadError as e:
                flash(str(e), "error")
                return render_template("admin/profile_form.html", form=form, profile=profile)

        if form.cv.data:
            try:
                filename = save_upload(form.cv.data, kind="document")
                delete_upload(profile.cv_filename)
                profile.cv_filename = filename
            except UploadError as e:
                flash(str(e), "error")
                return render_template("admin/profile_form.html", form=form, profile=profile)

        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for("admin.edit_profile"))

    return render_template("admin/profile_form.html", form=form, profile=profile)


# ------------------------------------------------------------------- Skills
@admin_bp.route("/skills")
def list_skills():
    skills = Skill.query.order_by(Skill.order.asc(), Skill.id.asc()).all()
    return render_template("admin/skills_list.html", skills=skills)


@admin_bp.route("/skills/add", methods=["GET", "POST"])
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill()
        form.populate_obj(skill)
        db.session.add(skill)
        db.session.commit()
        flash("Compétence ajoutée.", "success")
        return redirect(url_for("admin.list_skills"))
    return render_template("admin/skill_form.html", form=form, is_new=True)


@admin_bp.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
def edit_skill(skill_id):
    skill = db.session.get(Skill, skill_id) or abort(404)
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        form.populate_obj(skill)
        db.session.commit()
        flash("Compétence mise à jour.", "success")
        return redirect(url_for("admin.list_skills"))
    return render_template("admin/skill_form.html", form=form, is_new=False, item=skill)


@admin_bp.route("/skills/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    skill = db.session.get(Skill, skill_id) or abort(404)
    db.session.delete(skill)
    db.session.commit()
    flash("Compétence supprimée.", "success")
    return redirect(url_for("admin.list_skills"))


# --------------------------------------------------------------- Experience
@admin_bp.route("/experiences")
def list_experiences():
    experiences = Experience.query.order_by(Experience.order.asc(), Experience.start_date.desc()).all()
    return render_template("admin/experiences_list.html", experiences=experiences)


@admin_bp.route("/experiences/add", methods=["GET", "POST"])
def add_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        experience = Experience()
        form.populate_obj(experience)
        db.session.add(experience)
        db.session.commit()
        flash("Expérience ajoutée.", "success")
        return redirect(url_for("admin.list_experiences"))
    return render_template("admin/experience_form.html", form=form, is_new=True)


@admin_bp.route("/experiences/<int:experience_id>/edit", methods=["GET", "POST"])
def edit_experience(experience_id):
    experience = db.session.get(Experience, experience_id) or abort(404)
    form = ExperienceForm(obj=experience)
    if form.validate_on_submit():
        form.populate_obj(experience)
        db.session.commit()
        flash("Expérience mise à jour.", "success")
        return redirect(url_for("admin.list_experiences"))
    return render_template("admin/experience_form.html", form=form, is_new=False, item=experience)


@admin_bp.route("/experiences/<int:experience_id>/delete", methods=["POST"])
def delete_experience(experience_id):
    experience = db.session.get(Experience, experience_id) or abort(404)
    db.session.delete(experience)
    db.session.commit()
    flash("Expérience supprimée.", "success")
    return redirect(url_for("admin.list_experiences"))


# ------------------------------------------------------------------ Projects
@admin_bp.route("/projects")
def list_projects():
    projects = Project.query.order_by(Project.order.asc(), Project.id.asc()).all()
    return render_template("admin/projects_list.html", projects=projects)


@admin_bp.route("/projects/add", methods=["GET", "POST"])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        form.populate_obj(project)
        project.image_filename = None
        if form.image.data:
            try:
                project.image_filename = save_upload(form.image.data, kind="image")
            except UploadError as e:
                flash(str(e), "error")
                return render_template("admin/project_form.html", form=form, is_new=True)
        db.session.add(project)
        db.session.commit()
        flash("Projet ajouté.", "success")
        return redirect(url_for("admin.list_projects"))
    return render_template("admin/project_form.html", form=form, is_new=True)


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    project = db.session.get(Project, project_id) or abort(404)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        image_filename = project.image_filename
        form.populate_obj(project)
        project.image_filename = image_filename
        if form.image.data:
            try:
                filename = save_upload(form.image.data, kind="image")
                delete_upload(project.image_filename)
                project.image_filename = filename
            except UploadError as e:
                flash(str(e), "error")
                return render_template("admin/project_form.html", form=form, is_new=False, item=project)
        db.session.commit()
        flash("Projet mis à jour.", "success")
        return redirect(url_for("admin.list_projects"))
    return render_template("admin/project_form.html", form=form, is_new=False, item=project)


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    project = db.session.get(Project, project_id) or abort(404)
    delete_upload(project.image_filename)
    db.session.delete(project)
    db.session.commit()
    flash("Projet supprimé.", "success")
    return redirect(url_for("admin.list_projects"))


# ----------------------------------------------------------------- Education
@admin_bp.route("/education")
def list_education():
    items = Education.query.order_by(Education.order.asc(), Education.id.asc()).all()
    return render_template("admin/education_list.html", items=items)


@admin_bp.route("/education/add", methods=["GET", "POST"])
def add_education():
    form = EducationForm()
    if form.validate_on_submit():
        education = Education()
        form.populate_obj(education)
        db.session.add(education)
        db.session.commit()
        flash("Formation ajoutée.", "success")
        return redirect(url_for("admin.list_education"))
    return render_template("admin/education_form.html", form=form, is_new=True)


@admin_bp.route("/education/<int:education_id>/edit", methods=["GET", "POST"])
def edit_education(education_id):
    education = db.session.get(Education, education_id) or abort(404)
    form = EducationForm(obj=education)
    if form.validate_on_submit():
        form.populate_obj(education)
        db.session.commit()
        flash("Formation mise à jour.", "success")
        return redirect(url_for("admin.list_education"))
    return render_template("admin/education_form.html", form=form, is_new=False, item=education)


@admin_bp.route("/education/<int:education_id>/delete", methods=["POST"])
def delete_education(education_id):
    education = db.session.get(Education, education_id) or abort(404)
    db.session.delete(education)
    db.session.commit()
    flash("Formation supprimée.", "success")
    return redirect(url_for("admin.list_education"))


# -------------------------------------------------------------- Testimonials
@admin_bp.route("/testimonials")
def list_testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.order.asc(), Testimonial.id.asc()).all()
    return render_template("admin/testimonials_list.html", testimonials=testimonials)


@admin_bp.route("/testimonials/add", methods=["GET", "POST"])
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        testimonial = Testimonial()
        form.populate_obj(testimonial)
        db.session.add(testimonial)
        db.session.commit()
        flash("Témoignage ajouté.", "success")
        return redirect(url_for("admin.list_testimonials"))
    return render_template("admin/testimonial_form.html", form=form, is_new=True)


@admin_bp.route("/testimonials/<int:testimonial_id>/edit", methods=["GET", "POST"])
def edit_testimonial(testimonial_id):
    testimonial = db.session.get(Testimonial, testimonial_id) or abort(404)
    form = TestimonialForm(obj=testimonial)
    if form.validate_on_submit():
        form.populate_obj(testimonial)
        db.session.commit()
        flash("Témoignage mis à jour.", "success")
        return redirect(url_for("admin.list_testimonials"))
    return render_template("admin/testimonial_form.html", form=form, is_new=False, item=testimonial)


@admin_bp.route("/testimonials/<int:testimonial_id>/delete", methods=["POST"])
def delete_testimonial(testimonial_id):
    testimonial = db.session.get(Testimonial, testimonial_id) or abort(404)
    db.session.delete(testimonial)
    db.session.commit()
    flash("Témoignage supprimé.", "success")
    return redirect(url_for("admin.list_testimonials"))


# ----------------------------------------------------------------- Interests
@admin_bp.route("/interests")
def list_interests():
    interests = Interest.query.order_by(Interest.order.asc(), Interest.id.asc()).all()
    return render_template("admin/interests_list.html", interests=interests)


@admin_bp.route("/interests/add", methods=["GET", "POST"])
def add_interest():
    form = InterestForm()
    if form.validate_on_submit():
        interest = Interest()
        form.populate_obj(interest)
        db.session.add(interest)
        db.session.commit()
        flash("Centre d'intérêt ajouté.", "success")
        return redirect(url_for("admin.list_interests"))
    return render_template("admin/interest_form.html", form=form, is_new=True)


@admin_bp.route("/interests/<int:interest_id>/edit", methods=["GET", "POST"])
def edit_interest(interest_id):
    interest = db.session.get(Interest, interest_id) or abort(404)
    form = InterestForm(obj=interest)
    if form.validate_on_submit():
        form.populate_obj(interest)
        db.session.commit()
        flash("Centre d'intérêt mis à jour.", "success")
        return redirect(url_for("admin.list_interests"))
    return render_template("admin/interest_form.html", form=form, is_new=False, item=interest)


@admin_bp.route("/interests/<int:interest_id>/delete", methods=["POST"])
def delete_interest(interest_id):
    interest = db.session.get(Interest, interest_id) or abort(404)
    db.session.delete(interest)
    db.session.commit()
    flash("Centre d'intérêt supprimé.", "success")
    return redirect(url_for("admin.list_interests"))


# ---------------------------------------------------------------- Blog posts
@admin_bp.route("/blog")
def list_blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("admin/blog_list.html", posts=posts)


@admin_bp.route("/blog/add", methods=["GET", "POST"])
def add_blog_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        if BlogPost.query.filter_by(slug=form.slug.data.strip()).first():
            flash("Ce slug est déjà utilisé par un autre article.", "error")
            return render_template("admin/blog_form.html", form=form, is_new=True)
        post = BlogPost()
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash("Article ajouté.", "success")
        return redirect(url_for("admin.list_blog_posts"))
    return render_template("admin/blog_form.html", form=form, is_new=True)


@admin_bp.route("/blog/<int:post_id>/edit", methods=["GET", "POST"])
def edit_blog_post(post_id):
    post = db.session.get(BlogPost, post_id) or abort(404)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        existing = BlogPost.query.filter_by(slug=form.slug.data.strip()).first()
        if existing and existing.id != post.id:
            flash("Ce slug est déjà utilisé par un autre article.", "error")
            return render_template("admin/blog_form.html", form=form, is_new=False, item=post)
        form.populate_obj(post)
        db.session.commit()
        flash("Article mis à jour.", "success")
        return redirect(url_for("admin.list_blog_posts"))
    return render_template("admin/blog_form.html", form=form, is_new=False, item=post)


@admin_bp.route("/blog/<int:post_id>/delete", methods=["POST"])
def delete_blog_post(post_id):
    post = db.session.get(BlogPost, post_id) or abort(404)
    db.session.delete(post)
    db.session.commit()
    flash("Article supprimé.", "success")
    return redirect(url_for("admin.list_blog_posts"))


# --------------------------------------------------------- Contact messages
@admin_bp.route("/messages")
def list_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages_list.html", messages=messages)


@admin_bp.route("/messages/<int:message_id>/toggle-read", methods=["POST"])
def toggle_message_read(message_id):
    message = db.session.get(ContactMessage, message_id) or abort(404)
    message.is_read = not message.is_read
    db.session.commit()
    return redirect(url_for("admin.list_messages"))


@admin_bp.route("/messages/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):
    message = db.session.get(ContactMessage, message_id) or abort(404)
    db.session.delete(message)
    db.session.commit()
    flash("Message supprimé.", "success")
    return redirect(url_for("admin.list_messages"))
