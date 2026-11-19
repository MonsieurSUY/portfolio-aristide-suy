"""Render the public site to plain HTML files in ./dist (deployable anywhere).

French lives at "/", English at "/en/". Run via publish.py or directly:
    python export_static.py
"""
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from app import create_app
from app.models import BlogPost, Profile

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PUBLIC_URL = "bikoue.jsph.site"


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    app = create_app()
    app.config.update(
        STATIC_EXPORT=True, LOCAL_ADMIN=False, SERVER_NAME=PUBLIC_URL,
        PREFERRED_URL_SCHEME="https", SESSION_COOKIE_SECURE=False,
    )

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    with app.app_context():
        profile = Profile.query.first()
        cv_name = f"CV-{slugify(profile.full_name)}.pdf" if profile else "cv.pdf"
        app.config["CV_STATIC_URL"] = "/" + cv_name
        slugs = [p.slug for p in BlogPost.query.filter_by(published=True).all()]

    # Static assets (css, js, images, uploads)
    shutil.copytree(ROOT / "app" / "static", DIST / "static",
                    ignore=shutil.ignore_patterns(".gitkeep"))
    if profile and profile.cv_filename:
        shutil.copy(ROOT / "app" / "static" / "uploads" / profile.cv_filename, DIST / cv_name)

    client = app.test_client()
    for lang, prefix in (("fr", ""), ("en", "en/")):
        app.config["FORCE_LANG"] = lang
        res = client.get("/")
        assert res.status_code == 200, f"/ ({lang}) -> {res.status_code}"
        write(DIST / prefix / "index.html", res.get_data(as_text=True))
        for slug in slugs:
            res = client.get(f"/blog/{slug}")
            assert res.status_code == 200, f"/blog/{slug} ({lang}) -> {res.status_code}"
            write(DIST / prefix / "blog" / slug / "index.html", res.get_data(as_text=True))

    app.config["FORCE_LANG"] = "fr"
    write(DIST / "404.html", client.get("/__page-introuvable__").get_data(as_text=True))

    base = f"https://{PUBLIC_URL}"
    urls = [f"{base}/", f"{base}/en/"] + [f"{base}/blog/{s}/" for s in slugs] + [f"{base}/en/blog/{s}/" for s in slugs]
    sitemap = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    write(DIST / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>')
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    write(DIST / "vercel.json", """{
  "cleanUrls": true,
  "redirects": [
    { "source": "/favicon.ico", "destination": "/static/img/favicon.svg", "permanent": false }
  ]
}
""")
    print(f"Site statique généré dans {DIST} ({len(slugs)} article(s) de blog)")


if __name__ == "__main__":
    sys.exit(main())
