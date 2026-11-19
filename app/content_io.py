"""Export / import of the editable site content as a JSON snapshot.

The snapshot (content/content.json) is what gets committed to Git, so the site
can be rebuilt on another PC. Contact messages and admin accounts are NOT
included (private data).
"""
import json
from datetime import date, datetime
from pathlib import Path

from app.extensions import db
from app.models import (
    Profile, Skill, Experience, Project, Education, Testimonial, Interest, BlogPost,
)

MODELS = [Profile, Skill, Experience, Project, Education, Testimonial, Interest, BlogPost]
CONTENT_FILE = Path(__file__).resolve().parent.parent / "content" / "content.json"


def _to_json(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def export_content(path=CONTENT_FILE):
    data = {}
    for model in MODELS:
        rows = []
        for obj in model.query.order_by(model.id).all():
            rows.append({c.name: _to_json(getattr(obj, c.name)) for c in model.__table__.columns})
        data[model.__tablename__] = rows
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def import_content(path=CONTENT_FILE, replace=False):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for model in MODELS:
        if replace:
            model.query.delete()
        elif model.query.first() is not None:
            continue  # never overwrite existing content unless asked
        for row in data.get(model.__tablename__, []):
            values = {}
            for col in model.__table__.columns:
                value = row.get(col.name)
                if value is not None and isinstance(col.type, db.DateTime):
                    value = datetime.fromisoformat(value)
                elif value is not None and isinstance(col.type, db.Date):
                    value = date.fromisoformat(value)
                values[col.name] = value
            db.session.add(model(**values))
    db.session.commit()
