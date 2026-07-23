"""Entry point for running the app locally or under a WSGI server (gunicorn, waitress...)."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
