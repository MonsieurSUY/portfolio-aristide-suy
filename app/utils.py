"""File upload helpers: extension/size validation and safe storage."""
import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


class UploadError(Exception):
    pass


def _validate(file_storage, allowed_extensions, max_size_bytes):
    filename = file_storage.filename
    if not filename:
        raise UploadError("Aucun fichier sélectionné.")

    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed_extensions:
        raise UploadError(
            f"Extension .{ext} non autorisée. Autorisées : {', '.join(sorted(allowed_extensions))}."
        )

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > max_size_bytes:
        raise UploadError(f"Fichier trop volumineux ({size // 1024} Ko, max {max_size_bytes // 1024} Ko).")

    return ext


def save_upload(file_storage, kind="image"):
    """Validate and persist an uploaded file to /static/uploads.

    kind: "image" or "document" (PDF). Returns the stored filename.
    """
    if kind == "image":
        allowed = current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
        max_size = current_app.config["MAX_IMAGE_SIZE_BYTES"]
    elif kind == "document":
        allowed = current_app.config["ALLOWED_DOCUMENT_EXTENSIONS"]
        max_size = current_app.config["MAX_DOCUMENT_SIZE_BYTES"]
    else:
        raise ValueError("kind must be 'image' or 'document'")

    ext = _validate(file_storage, allowed, max_size)

    safe_base = secure_filename(file_storage.filename.rsplit(".", 1)[0]) or kind
    filename = f"{safe_base}-{uuid.uuid4().hex[:8]}.{ext}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    file_storage.save(os.path.join(upload_folder, filename))
    return filename


def delete_upload(filename):
    if not filename:
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass
