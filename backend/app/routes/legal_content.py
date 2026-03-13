"""
Public legal content routes.

Loads language-specific legal HTML files (imprint, data protection, terms of service)
from a configurable filesystem path.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from config import config

router = APIRouter(prefix="/config/legal", tags=["configuration"])

_ALLOWED_DOCUMENTS = {"imprint", "data-protection", "terms-of-service"}


@router.get("/{document_type}", response_class=HTMLResponse)
async def get_legal_document(
    document_type: str,
    lang: str = Query(None, description="Language code (en or de)"),
):
    """Return the configured HTML content for one legal document and language."""
    normalized_document_type = (document_type or "").strip().lower()
    if normalized_document_type not in _ALLOWED_DOCUMENTS:
        raise HTTPException(status_code=404, detail="Legal document not found")

    requested_lang = (lang or config.DEFAULT_LANGUAGE).strip().lower()
    legal_file_path = config.resolve_legal_file_path(normalized_document_type, requested_lang)

    try:
        # Prevent accidental path escapes if templates are misconfigured.
        legal_file_path.relative_to(config.LEGAL_CONTENT_DIRECTORY)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail="Invalid legal content path configuration") from exc

    if not legal_file_path.exists() or not legal_file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Legal content file not found for '{normalized_document_type}' ({requested_lang})",
        )

    try:
        content = legal_file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise HTTPException(status_code=500, detail="Failed to read legal content file") from exc

    return HTMLResponse(content=content)
