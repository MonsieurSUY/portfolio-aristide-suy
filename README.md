# Portfolio / CV en ligne — Flask

Site personnel one-page (portfolio + CV en ligne) entièrement administrable, construit avec Flask, SQLAlchemy et Tailwind CSS. Bilingue FR/EN, mode sombre, animations discrètes au scroll, SEO de base, et un espace d'administration complet pour gérer tout le contenu sans toucher au code.

## Sommaire

- [Stack technique](#stack-technique)
- [Installation](#installation)
- [Lancer le site en local](#lancer-le-site-en-local)
- [Comment ajouter / modifier du contenu](#comment-ajouter--modifier-du-contenu)
- [Structure du projet](#structure-du-projet)
- [Choix de conception](#choix-de-conception)
- [Passage en production](#passage-en-production)

## Stack technique

- **Backend** : Python 3 + Flask, organisé en blueprints (`public`, `admin`, `auth`)
- **ORM / DB** : Flask-SQLAlchemy, SQLite en développement (`instance/app.db`, dossier standard de Flask pour les fichiers locaux, déjà exclu de git), compatible PostgreSQL en production via `DATABASE_URL`
- **Migrations** : Flask-Migrate (Alembic)
- **Auth admin** : Flask-Login + mots de passe hashés (`werkzeug.security`) + Flask-Limiter sur la connexion
- **Formulaires** : Flask-WTF (CSRF inclus)
- **Templates** : Jinja2
- **CSS** : Tailwind CSS via CDN (Play CDN, plugin typography), polices Google Fonts (Sora / Inter)
- **i18n** : dictionnaire FR/EN maison (`app/i18n.py`) + champs `_fr` / `_en` sur les modèles
- **Markdown** : `Markdown` + `bleach` (nettoyage anti-XSS) pour le champ "À propos" et le blog

## Installation

Depuis la racine du projet (`MonSite/`) :

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
copy .env.example .env
```

Ouvrez `.env` et personnalisez au minimum `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` et `SITE_URL`.

## Lancer le site en local

Toujours dans l'environnement virtuel activé, avec `FLASK_APP` défini sur `wsgi.py` :

```bash
set FLASK_APP=wsgi.py
```

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

```bash
flask create-admin
```

Cette commande crée le compte admin unique à partir des identifiants du `.env` (`ADMIN_USERNAME` / `ADMIN_PASSWORD`). Relancez-la avec les mêmes identifiants pour réinitialiser le mot de passe.

```bash
flask seed-content
```

Insère le contenu de départ (profil, compétences, expériences, formations/certifications, centres d'intérêt) si la base est vide — sans rien écraser si elle contient déjà des données. **Ce contenu reste entièrement modifiable via l'espace admin.**

```bash
flask run
```

Le site est alors disponible sur http://localhost:5000, l'espace admin sur http://localhost:5000/auth/login.

> Récapitulatif : 6 commandes après l'installation des dépendances (`db init`, `db migrate`, `db upgrade`, `create-admin`, `seed-content`, `run`) — les trois premières ne sont nécessaires qu'une fois.

## Comment ajouter / modifier du contenu

1. Connectez-vous sur `/auth/login` avec les identifiants définis dans `.env`.
2. Le tableau de bord (`/admin`) liste chaque type de contenu avec son nombre d'éléments.
3. **Profil / Hero / À propos** : formulaire unique (nom, titre, accroche, texte "à propos" en Markdown, disponibilité, photo, CV en PDF, liens de contact).
4. **Compétences, Expériences, Projets, Formations, Témoignages, Centres d'intérêt, Articles de blog** : chaque section a sa liste, un bouton "Ajouter", et pour chaque élément "Modifier" / "Supprimer" (avec confirmation).
5. Les éléments avec un champ **Ordre** (compétences, expériences, projets, formations) s'affichent triés par cette valeur croissante sur le site public — changez ce nombre pour réorganiser.
6. Les **témoignages** et **articles de blog** ont une case "Publié" : seuls les éléments publiés apparaissent sur le site (et la section entière ne s'affiche pas si elle est vide).
7. Les **messages de contact** reçus via le formulaire public apparaissent dans `/admin/messages`, triés du plus récent au plus ancien, avec un bouton pour les marquer lu/non lu et les supprimer.
8. Tous les champs de texte visibles sur le site existent en deux versions (FR / EN) : remplissez les deux pour un rendu correct dans les deux langues.
9. Les images (photo de profil, captures d'écran de projets) et le CV sont uploadés directement depuis les formulaires ; ils sont validés (type et taille) et stockés dans `app/static/uploads/`.

## Structure du projet

```
MonSite/
├── app/
│   ├── __init__.py          # application factory
│   ├── config.py            # configuration via variables d'environnement
│   ├── extensions.py        # instances SQLAlchemy, Migrate, LoginManager, Limiter
│   ├── models.py            # modèles SQLAlchemy (avec champs _fr / _en)
│   ├── forms.py             # formulaires Flask-WTF
│   ├── i18n.py               # traductions de l'interface (FR/EN)
│   ├── utils.py              # validation et stockage des fichiers uploadés
│   ├── cli.py                 # commandes `flask create-admin` / `flask seed-content`
│   ├── blueprints/
│   │   ├── public/           # site public (one-page + articles de blog)
│   │   ├── admin/            # espace d'administration (CRUD complet)
│   │   └── auth/             # connexion / déconnexion
│   ├── templates/
│   │   ├── base.html
│   │   ├── public/
│   │   └── admin/
│   └── static/
│       ├── css/, js/, img/
│       └── uploads/          # fichiers uploadés depuis l'admin
├── migrations/                # migrations Alembic (générées par Flask-Migrate)
├── seed.py                    # contenu de départ (profil, compétences, expériences...)
├── wsgi.py                    # point d'entrée de l'application
├── requirements.txt
├── .env.example
└── README.md
```

## Choix de conception

- **Bilinguisme** : plutôt que Flask-Babel (fichiers `.po`/`.mo`, compilation, etc.), un dictionnaire Python (`app/i18n.py`) gère les textes fixes de l'interface, et chaque modèle stocke ses champs de contenu en double (`_fr` / `_en`) avec une propriété (`.title`, `.name`, ...) qui retourne la version correspondant à la langue courante (stockée en session). Plus simple à maintenir pour un site de cette taille, sans dépendance de compilation.
- **Tailwind via CDN** : évite une étape de build (npm, PostCSS) pour rester dans les "5-6 commandes" de lancement demandées, tout en gardant un design entièrement personnalisé (pas de thème par défaut) grâce à la configuration inline (`tailwind.config`) et au plugin typography.
- **Markdown + bleach** : le champ "À propos" et le contenu des articles de blog acceptent du Markdown, converti en HTML puis nettoyé (liste blanche de balises/attributs) pour éviter toute injection, même si seul l'admin authentifié peut écrire ce contenu.
- **SQLite → PostgreSQL** : toute la configuration passe par `DATABASE_URL` (`Config.SQLALCHEMY_DATABASE_URI`), donc changer de base ne nécessite qu'une variable d'environnement et l'installation du driver adéquat (`psycopg2-binary`, commenté dans `requirements.txt`).
- **Uploads locaux** : stockage dans `app/static/uploads/`, noms de fichiers assainis (`secure_filename` + suffixe unique), extensions et tailles validées côté serveur (`app/utils.py`) — adapté à un déploiement mono-serveur ; pour un déploiement multi-instances, ce dossier devrait être remplacé par un stockage objet (S3, etc.).
- **Rate limiting basique** : Flask-Limiter limite la route de connexion à 10 tentatives par minute et par IP, suffisant pour dissuader le brute force sur un site personnel sans complexifier l'infrastructure (pas de Redis requis en développement).

## Passage en production

- Définissez `FLASK_ENV=production` (active les cookies de session sécurisés).
- Configurez `DATABASE_URL` vers une base PostgreSQL (le pilote `psycopg2-binary` est déjà dans `requirements.txt`).
- Servez l'application avec un serveur WSGI de production (`gunicorn wsgi:app`, déjà dans `requirements.txt`) derrière un reverse proxy géré par la plateforme d'hébergement.
- Configurez `RATELIMIT_STORAGE_URI` vers Redis si vous déployez plusieurs instances/process.
- Générez une `SECRET_KEY` forte et changez le mot de passe admin par défaut.
- Renseignez `SITE_URL` avec le nom de domaine réel pour que `sitemap.xml`, `robots.txt` et les balises Open Graph pointent au bon endroit.

## Déploiement sur Render

Le fichier [`render.yaml`](render.yaml) décrit automatiquement le service web et la base PostgreSQL (Render Blueprint).

1. Poussez ce dépôt sur GitHub.
2. Sur [render.com](https://render.com) : **New** → **Blueprint**, puis sélectionnez le dépôt. Render lit `render.yaml` et propose de créer le service web + la base de données.
3. Renseignez la variable `ADMIN_PASSWORD` (marquée `sync: false`, donc jamais commitée dans le code) avec un mot de passe fort de votre choix.
4. Lancez le déploiement. À chaque build, Render exécute automatiquement `flask db upgrade`, `flask seed-content` (idempotent) et `flask create-admin` avant de démarrer le serveur — aucune commande manuelle supplémentaire n'est nécessaire.
5. Une fois en ligne, connectez-vous sur `https://<votre-service>.onrender.com/auth/login` avec `admin` / le mot de passe défini à l'étape 3.
6. Si l'URL générée par Render diffère de `aristide-suy-portfolio.onrender.com`, mettez à jour la variable d'environnement `SITE_URL` dans le tableau de bord Render (Settings → Environment) pour que le sitemap et les balises Open Graph restent corrects.

**Limite à connaître (plan gratuit Render)** : le disque du service web n'est pas persistant entre deux déploiements — un fichier envoyé depuis l'admin (nouvelle photo, nouveau CV, image de projet) survit tant qu'aucun nouveau déploiement n'a lieu, mais sera perdu au prochain `git push`. Le contenu textuel (profil, compétences, expériences...) n'est pas concerné : il vit dans PostgreSQL, qui est un service séparé et persistant. Deux options si ça devient gênant : passer le service web sur un plan payant avec disque persistant, ou stocker les fichiers uploadés sur un service externe (S3, Cloudinary...).
