"""Lightweight FR/EN dictionary-based translation system for static UI strings.

Dynamic content (skills, projects, ...) stores its own `_fr` / `_en` columns
directly on the models instead - see models.py.
"""
from flask import session, current_app

TRANSLATIONS = {
    "nav.about": {"fr": "À propos", "en": "About"},
    "nav.skills": {"fr": "Compétences", "en": "Skills"},
    "nav.experience": {"fr": "Parcours", "en": "Experience"},
    "nav.projects": {"fr": "Projets", "en": "Projects"},
    "nav.education": {"fr": "Formation", "en": "Education"},
    "nav.testimonials": {"fr": "Témoignages", "en": "Testimonials"},
    "nav.interests": {"fr": "Centres d'intérêt", "en": "Interests"},
    "nav.blog": {"fr": "Blog", "en": "Blog"},
    "nav.contact": {"fr": "Contact", "en": "Contact"},

    "hero.download_cv": {"fr": "Télécharger mon CV", "en": "Download my résumé"},
    "hero.contact_me": {"fr": "Me contacter", "en": "Contact me"},
    "hero.cv_unavailable": {"fr": "CV bientôt disponible", "en": "Résumé coming soon"},

    "about.title": {"fr": "À propos", "en": "About"},

    "skills.title": {"fr": "Compétences", "en": "Skills"},
    "skills.level.debutant": {"fr": "Débutant", "en": "Beginner"},
    "skills.level.confirme": {"fr": "Confirmé", "en": "Intermediate"},
    "skills.level.expert": {"fr": "Expert", "en": "Expert"},

    "experience.title": {"fr": "Parcours professionnel", "en": "Professional experience"},
    "experience.present": {"fr": "En cours", "en": "Present"},

    "projects.title": {"fr": "Projets", "en": "Projects"},
    "projects.demo": {"fr": "Démo", "en": "Demo"},
    "projects.source": {"fr": "Code source", "en": "Source code"},
    "projects.more": {"fr": "En savoir plus", "en": "Read more"},
    "projects.less": {"fr": "Réduire", "en": "Show less"},

    "education.title": {"fr": "Formation, diplômes et certifications", "en": "Education & certifications"},
    "education.verify": {"fr": "Vérifier", "en": "Verify"},
    "education.category.diplome": {"fr": "Diplômes", "en": "Degrees"},
    "education.category.certification": {"fr": "Certifications", "en": "Certifications"},
    "education.category.formation": {"fr": "Formations suivies", "en": "Trainings attended"},

    "testimonials.title": {"fr": "Témoignages", "en": "Testimonials"},

    "interests.title": {"fr": "Centres d'intérêt", "en": "Interests"},

    "blog.title": {"fr": "Blog & notes", "en": "Blog & notes"},
    "blog.read_more": {"fr": "Lire l'article", "en": "Read article"},
    "blog.back": {"fr": "Retour à l'accueil", "en": "Back to home"},

    "contact.title": {"fr": "Contact", "en": "Contact"},
    "contact.subtitle": {
        "fr": "Une question, une opportunité ? Écrivez-moi.",
        "en": "A question, an opportunity? Get in touch.",
    },
    "contact.name": {"fr": "Nom", "en": "Name"},
    "contact.email": {"fr": "Email", "en": "Email"},
    "contact.subject": {"fr": "Sujet", "en": "Subject"},
    "contact.message": {"fr": "Message", "en": "Message"},
    "contact.send": {"fr": "Envoyer le message", "en": "Send message"},
    "contact.write_me": {"fr": "Écrivez-moi par email", "en": "Email me"},
    "contact.mailto_subject": {"fr": "Contact depuis votre portfolio", "en": "Contact from your portfolio"},
    "contact.success": {
        "fr": "Merci ! Votre message a bien été envoyé.",
        "en": "Thanks! Your message has been sent.",
    },
    "contact.error": {
        "fr": "Une erreur est survenue, merci de réessayer.",
        "en": "Something went wrong, please try again.",
    },

    "footer.rights": {"fr": "Tous droits réservés.", "en": "All rights reserved."},
    "footer.made_with": {"fr": "Conçu avec Flask & Tailwind CSS", "en": "Built with Flask & Tailwind CSS"},

    "theme.toggle": {"fr": "Changer de thème", "en": "Toggle theme"},
    "lang.toggle": {"fr": "Changer de langue", "en": "Toggle language"},

    "error.404.title": {"fr": "Page introuvable", "en": "Page not found"},
    "error.404.text": {
        "fr": "La page que vous cherchez n'existe pas ou a été déplacée.",
        "en": "The page you're looking for doesn't exist or has moved.",
    },
    "error.500.title": {"fr": "Erreur serveur", "en": "Server error"},
    "error.500.text": {
        "fr": "Une erreur inattendue est survenue. Merci de réessayer plus tard.",
        "en": "An unexpected error occurred. Please try again later.",
    },
    "error.back_home": {"fr": "Retour à l'accueil", "en": "Back to home"},

    "availability.disponible": {"fr": "Disponible", "en": "Available"},
    "availability.en_poste": {"fr": "En poste", "en": "Employed"},
    "availability.ouvert": {"fr": "Ouvert aux opportunités", "en": "Open to opportunities"},
}


def get_locale():
    forced = current_app.config.get("FORCE_LANG")  # set by the static export
    if forced:
        return forced
    lang = session.get("lang")
    if lang in current_app.config["LANGUAGES"]:
        return lang
    return current_app.config["DEFAULT_LANGUAGE"]


def t(key):
    lang = get_locale()
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get("fr", key))
