# Portfolio — Bi Koué Jean Noël Aristide Suy

Site en ligne : **https://bikoue.jsph.site** (site statique hébergé gratuitement sur Vercel, sans expiration).

## Comment ça marche

- Le site public est **généré en HTML** à partir d'une application Flask qui tourne **uniquement sur votre PC**.
- Vous modifiez le contenu dans l'espace admin local, puis vous cliquez sur **Publier le site** : le site est reconstruit, mis en ligne sur Vercel et sauvegardé sur Git.
- Le contenu modifiable est sauvegardé dans `content/content.json` (versionné), les images et le CV dans `app/static/uploads/`.

## Utilisation au quotidien

1. Double-cliquez sur l'icône **Mon Portfolio - Admin** (Bureau). L'admin s'ouvre dans le navigateur, déjà connecté.
2. Modifiez compétences, expériences, projets, formations, photo, CV, etc.
3. Cliquez sur **Publier le site** (tableau de bord ou menu de gauche). Comptez environ une minute.
4. Fermez la fenêtre noire quand vous avez fini (elle arrête le serveur local).

Le formulaire de contact est remplacé sur le site en ligne par un bouton « Écrivez-moi par email » (aucune base de données en ligne).

## Changer de PC

1. Installer Python 3, Git, Node.js, puis : `npm i -g vercel` et `vercel login` (une fois).
2. `git clone https://github.com/MonsieurSUY/portfolio-aristide-suy.git`
3. Double-cliquer sur `Installer.bat` : il crée l'environnement, restaure le contenu depuis `content/content.json` et recrée l'icône du Bureau.

## Commandes utiles

```bash
python publish.py              # tout faire : sauvegarde du contenu, build, Vercel, Git
python publish.py --no-deploy  # sans mise en ligne
python export_static.py        # génère seulement le dossier dist/
flask export-content           # écrit content/content.json
flask import-content --replace # recharge la base depuis content/content.json
```

## Structure

- `app/` : application Flask (public, admin, auth), modèles, templates, assets
- `export_static.py` : génération du site statique (FR à `/`, EN à `/en/`)
- `publish.py` : pipeline de publication
- `deploy/` : icône, installateur, identifiant du projet Vercel
- `Lancer_Admin.bat` / `Installer.bat` : lanceur de l'admin et installation
