"""Seed the database with Bi Koué Jean Noël Aristide Suy's starter content
(sourced from his CV). Safe to run repeatedly: each block only inserts rows
if the corresponding table is still empty. Everything remains editable
through /admin afterwards.

Usage: flask seed-content   (or `python seed.py` inside an app context)
"""
from datetime import date

from app.extensions import db
from app.models import (
    Profile, Skill, Experience, Project, Education, Testimonial, Interest, BlogPost,
)


def run_seed():
    if Profile.query.first() is None:
        db.session.add(Profile(
            full_name="Bi Koué Jean Noël Aristide Suy",
            title_fr="Analyste Statisticien Économiste",
            title_en="Statistical Analyst & Economist",
            tagline_fr="Je transforme les données en outils d'aide au pilotage et à l'élaboration des politiques publiques.",
            tagline_en="I turn data into tools for steering decisions and shaping public policy.",
            about_fr=(
                "Analyste Statisticien - Économiste spécialisé dans l'analyse de données, les études "
                "sectorielles et l'appui à la décision. Expérimenté en administration publique et suivi "
                "de projets, je transforme les données en outils d'aide au pilotage et à l'élaboration "
                "des politiques publiques.\n\nRigoureux, polyvalent et orienté résultats."
            ),
            about_en=(
                "Statistical Analyst and Economist specialized in data analysis, sector studies and "
                "decision support. Experienced in public administration and project monitoring, I turn "
                "data into tools for steering decisions and shaping public policy.\n\nRigorous, "
                "versatile and results-driven."
            ),
            availability_fr="En poste",
            availability_en="Employed",
            email="jeanoelsuyaristide@gmail.com",
            phone="+225 07 69 59 65 24",
            linkedin_url="",
            github_url="",
            avatar_filename="avatar-aristide-ca28dd56.png",
            cv_filename="cv-aristide-e09c533f.pdf",
        ))

    if Skill.query.first() is None:
        skills = [
            # (name_fr, name_en, category_fr, category_en, level, order)
            ("Méthodologie d'enquêtes quantitatives et qualitatives", "Quantitative & qualitative survey methodology", "Statistique", "Statistics", None, 1),
            ("Collecte, traitement, analyse, diffusion et archivage de données", "Data collection, processing, analysis, dissemination & archiving", "Statistique", "Statistics", None, 2),
            ("Analyse descriptive de données", "Descriptive data analysis", "Statistique", "Statistics", None, 3),
            ("Interprétation et communication des données", "Data interpretation & communication", "Statistique", "Statistics", None, 4),
            ("Production de rapports d'analyse ; storytelling", "Analytical reporting & data storytelling", "Statistique", "Statistics", None, 5),

            ("Pack Office ; Excel avancé", "MS Office; Advanced Excel", "Informatique", "Software & Tools", "expert", 6),
            ("Tableau, Power BI, MS Project, QGIS", "Tableau, Power BI, MS Project, QGIS", "Informatique", "Software & Tools", "confirme", 7),
            ("CSPro, SuSo, Kobo Collect", "CSPro, SuSo, Kobo Collect", "Informatique", "Software & Tools", "confirme", 8),
            ("SPSS, STATA, SPAD", "SPSS, STATA, SPAD", "Informatique", "Software & Tools", "confirme", 9),
            ("Python, R, VBA, HTML, CSS, JS", "Python, R, VBA, HTML, CSS, JS", "Informatique", "Software & Tools", "confirme", 10),
            ("Photoshop, Premiere Pro, Illustrator", "Photoshop, Premiere Pro, Illustrator", "Informatique", "Software & Tools", "debutant", 11),

            ("Économie, management, démographie", "Economics, management, demography", "Technique", "Technical knowledge", None, 12),
            ("Développement web, bases de données", "Web development, databases", "Technique", "Technical knowledge", None, 13),
            ("Économétrie, marketing, data science", "Econometrics, marketing, data science", "Technique", "Technical knowledge", None, 14),

            ("Français", "French", "Langues", "Languages", "expert", 15),
            ("Anglais", "English", "Langues", "Languages", "confirme", 16),

            ("Discipline", "Discipline", "Qualités", "Soft skills", None, 17),
            ("Créativité", "Creativity", "Qualités", "Soft skills", None, 18),
            ("Travail en équipe", "Teamwork", "Qualités", "Soft skills", None, 19),
            ("Communication", "Communication", "Qualités", "Soft skills", None, 20),
            ("Orienté résultats", "Results-oriented", "Qualités", "Soft skills", None, 21),
            ("Curiosité technique", "Technical curiosity", "Qualités", "Soft skills", None, 22),
        ]
        for name_fr, name_en, cat_fr, cat_en, level, order in skills:
            db.session.add(Skill(
                name_fr=name_fr, name_en=name_en,
                category_fr=cat_fr, category_en=cat_en,
                level=level, order=order,
            ))

    if Experience.query.first() is None:
        db.session.add(Experience(
            role_fr="Formateur en entreprise", role_en="Corporate Trainer",
            company="Association des Gestionnaires des Ressources Humaines (AGRH)",
            location="Abidjan, Côte d'Ivoire",
            start_date=date(2026, 5, 1), end_date=None,
            description_fr="Animation de formations professionnelles en analyse de données et outils décisionnels.",
            description_en="Delivering professional training on data analysis and business intelligence tools.",
            achievements_fr="Formation Excel Avancé & Power BI\nAnalyse de données & conception de tableaux de bord",
            achievements_en="Advanced Excel & Power BI training\nData analysis & dashboard design",
            order=1,
        ))
        db.session.add(Experience(
            role_fr="Membre de la Task-Force — Système d'Information sur le Marché du Travail",
            role_en="Task Force Member — Labour Market Information System",
            company="Observatoire National de l'Emploi et de la Formation (ONEF)",
            location="Abidjan, Côte d'Ivoire",
            start_date=date(2025, 7, 1), end_date=date(2026, 6, 1),
            description_fr="Participation au projet de mise en place du Système d'Information sur le Marché du Travail.",
            description_en="Contributed to the project setting up the national Labour Market Information System.",
            achievements_fr=(
                "Création des structures de données au format SDMX\n"
                "Collecte de données auprès des institutions et ministères\n"
                "Vérification de la qualité et mise en ligne des données"
            ),
            achievements_en=(
                "Built SDMX-format data structures\n"
                "Collected data from institutions and ministries\n"
                "Checked data quality and published it online"
            ),
            order=2,
        ))
        db.session.add(Experience(
            role_fr="Consultant — Banque Mondiale, Projet PHAS", role_en="Consultant — World Bank, PHAS Project",
            company="Agence Nationale de la Statistique (ANStat)",
            location="Riviera Bonoumin, Abidjan",
            start_date=date(2024, 7, 1), end_date=None,
            description_fr="Appui à la collecte et au traitement de données statistiques nationales.",
            description_en="Supporting the collection and processing of national statistical data.",
            achievements_fr="Collecte et traitement de données (recensement et enquêtes)\nCalcul et publication des indicateurs conjoncturels",
            achievements_en="Data collection and processing (census and surveys)\nComputed and published short-term economic indicators",
            order=3,
        ))
        db.session.add(Experience(
            role_fr="Statisticien", role_en="Statistician",
            company="Polyclinique FARAH",
            location="Abidjan Marcory, Côte d'Ivoire",
            start_date=date(2024, 4, 1), end_date=date(2024, 6, 1),
            description_fr="Suivi statistique de l'activité des services de la polyclinique.",
            description_en="Statistical monitoring of the clinic's departmental activity.",
            achievements_fr="Collecte, traitement et analyse des données des services\nProduction de tableaux de bord et de rapports périodiques",
            achievements_en="Collected, processed and analyzed departmental data\nProduced dashboards and periodic reports",
            order=4,
        ))
        db.session.add(Experience(
            role_fr="Coordonnateur Général", role_en="General Coordinator",
            company="Complexe Commercial Ebenezer",
            location="Yopougon Keneya, Abidjan",
            start_date=date(2024, 2, 1), end_date=date(2024, 4, 1),
            description_fr="Coordination générale des activités commerciales du complexe.",
            description_en="General coordination of the commercial complex's activities.",
            achievements_fr="Coordination et supervision des activités des départements\nÉlaboration de stratégies commerciales et de gestion",
            achievements_en="Coordinated and supervised departmental activities\nDeveloped commercial and management strategies",
            order=5,
        ))
        db.session.add(Experience(
            role_fr="Junior Analyst (Finance & Stratégie)", role_en="Junior Analyst (Finance & Strategy)",
            company="SEVEN-CAP",
            location="Cocody Angré, Abidjan",
            start_date=date(2023, 9, 1), end_date=date(2024, 2, 1),
            description_fr="Appui aux missions de conseil en restructuration d'entreprises.",
            description_en="Supported corporate restructuring advisory engagements.",
            achievements_fr=(
                "Suivi, coordination et évaluation des opérations de restructuration\n"
                "Analyse des opérations et processus des entreprises\n"
                "Rédaction de rapports et de comptes rendus de réunions"
            ),
            achievements_en=(
                "Tracked, coordinated and evaluated restructuring operations\n"
                "Analyzed company operations and processes\n"
                "Drafted reports and meeting minutes"
            ),
            order=6,
        ))

    if Education.query.first() is None:
        education_rows = [
            # (institution, degree_fr, degree_en, year, verification_url, category, order)
            ("Institut Universitaire d'Abidjan (IUA)", "Master Économie du Développement (en cours)", "Master's in Development Economics (in progress)", "Depuis 2025", "", "diplome", 1),
            ("École Nationale Supérieure de Statistique et d'Économie Appliquée (ENSEA)", "Diplôme d'Analyste Statisticien (AS)", "Statistical Analyst (AS) Diploma", "2020 – 2023", "", "diplome", 2),
            ("École Nationale Supérieure de Statistique et d'Économie Appliquée (ENSEA)", "Diplôme d'Agent Technique de la Statistique (AT)", "Statistical Technical Officer (AT) Diploma", "2019 – 2020", "", "diplome", 3),
            ("Campus AFD (Agence Française de Développement)", "Concevoir un projet de développement respectueux de l'environnement et des populations", "Designing an Environmentally & Socially Responsible Development Project", "Janvier 2024", "", "certification", 4),
            ("Campus AFD (Agence Française de Développement)", "Suivi et évaluation d'un projet de développement", "Monitoring & Evaluation of a Development Project", "Février 2024", "", "certification", 5),
            ("OpenClassrooms", "Gérer un projet digital avec une méthodologie en cascade", "Managing a Digital Project with a Waterfall Methodology", "Janvier 2024", "", "certification", 6),
            ("OpenClassrooms", "Maîtriser les fondamentaux d'Excel & Excel avancé", "Excel Fundamentals & Advanced Excel", "Janvier 2024", "", "certification", 7),
            ("OpenClassrooms", "Réaliser des dashboards avec Power BI", "Building Dashboards with Power BI", "Février 2024", "", "certification", 8),
            ("PHASAOC — Volet UEMOA", "Introduction aux méthodes d'échantillonnage pour les enquêtes auprès des ménages", "Introduction to Sampling Methods for Household Surveys", "Février 2026", "", "formation", 9),
            ("PHASAOC — Volet UEMOA", "Mesurer le patrimoine des ménages pour analyser leur vulnérabilité", "Measuring Household Wealth to Assess Vulnerability", "Mars – Avril 2026", "", "formation", 10),
            ("Agence Nationale de la Statistique (ANStat)", "Renforcement de capacités sur le SDMX/ODP 2.0", "SDMX/ODP 2.0 Capacity Building", "Janvier 2026", "", "formation", 11),
        ]
        for institution, degree_fr, degree_en, year, verif, category, order in education_rows:
            db.session.add(Education(
                institution=institution, degree_fr=degree_fr, degree_en=degree_en,
                year=year, verification_url=verif, category=category, order=order,
            ))

    if Interest.query.first() is None:
        interests = [
            ("Échecs", "Chess", "♟️", 1),
            ("Vélo", "Cycling", "🚴", 2),
            ("Natation", "Swimming", "🏊", 3),
            ("Voyage", "Travel", "✈️", 4),
            ("Découverte", "Exploration", "🧭", 5),
            ("Animés", "Anime", "🎬", 6),
        ]
        for name_fr, name_en, icon, order in interests:
            db.session.add(Interest(name_fr=name_fr, name_en=name_en, icon=icon, order=order))

    # Projects, testimonials and blog posts are left empty on purpose: none
    # were provided on the CV. Add them through /admin whenever ready.

    db.session.commit()


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        run_seed()
        print("Contenu inséré.")
