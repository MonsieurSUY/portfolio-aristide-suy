"""Custom Flask CLI commands."""
import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import AdminUser


def register_cli(app):
    @app.cli.command("create-admin")
    @click.option("--username", default=None, help="Identifiant admin (sinon ADMIN_USERNAME du .env)")
    @click.option("--email", default=None, help="Email admin (sinon ADMIN_EMAIL du .env)")
    @click.option("--password", default=None, help="Mot de passe admin (sinon ADMIN_PASSWORD du .env)")
    @with_appcontext
    def create_admin(username, password, email):
        """Create (or reset the password of) the single admin account."""
        username = username or app.config["ADMIN_USERNAME"]
        email = email or app.config["ADMIN_EMAIL"]
        password = password or app.config["ADMIN_PASSWORD"]

        user = AdminUser.query.filter_by(username=username).first()
        if user:
            user.set_password(password)
            user.email = email
            db.session.commit()
            click.echo(f"Mot de passe mis à jour pour l'admin existant '{username}'.")
            return

        user = AdminUser(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Compte admin '{username}' créé avec succès.")

    @app.cli.command("seed-content")
    @with_appcontext
    def seed_content():
        """Populate empty tables with the site's starter content. Safe to re-run."""
        from seed import run_seed

        run_seed()
        click.echo("Contenu inséré (les tables déjà remplies n'ont pas été touchées).")

    @app.cli.command("export-content")
    @with_appcontext
    def export_content_cmd():
        """Write the editable content to content/content.json (versioned in Git)."""
        from app.content_io import export_content

        click.echo(f"Contenu exporté dans {export_content()}")

    @app.cli.command("import-content")
    @click.option("--replace", is_flag=True, help="Écrase le contenu existant.")
    @with_appcontext
    def import_content_cmd(replace):
        """Load content/content.json into the database (empty tables only, unless --replace)."""
        from app.content_io import import_content

        import_content(replace=replace)
        click.echo("Contenu importé.")
