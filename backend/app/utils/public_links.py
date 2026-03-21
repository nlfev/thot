"""
Utilities for public record links and QR code generation.
"""

import base64
import io
from uuid import UUID

import qrcode
from PIL import Image

from config import config

_BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_BASE62_BASE = len(_BASE62_ALPHABET)
QR_CODE_SIZE_MM = 35
QR_CODE_RENDER_DPI = 300


def encode_uuid_to_base62(record_id: UUID) -> str:
    """Encode a UUID into a compact base62 string."""
    number = record_id.int
    if number == 0:
        return _BASE62_ALPHABET[0]

    encoded = []
    while number > 0:
        number, remainder = divmod(number, _BASE62_BASE)
        encoded.append(_BASE62_ALPHABET[remainder])
    return "".join(reversed(encoded))


def decode_base62_to_uuid(value: str) -> UUID:
    """Decode a base62 string back into a UUID."""
    normalized = (value or "").strip()
    if not normalized:
        raise ValueError("Encoded record id is required")

    number = 0
    for character in normalized:
        try:
            digit = _BASE62_ALPHABET.index(character)
        except ValueError as exc:
            raise ValueError("Encoded record id contains invalid characters") from exc
        number = (number * _BASE62_BASE) + digit

    if number < 0 or number >= (1 << 128):
        raise ValueError("Encoded record id is out of range")

    return UUID(int=number)


def build_record_public_url(record_id: UUID) -> str:
    """Build the public frontend URL for a record."""
    encoded_id = encode_uuid_to_base62(record_id)
    return f"{config.FRONTEND_URL.rstrip('/')}/lit/{encoded_id}"


def build_record_qr_payload(signature: str | None, public_url: str) -> str:
    """Build QR payload containing signature and public link."""
    normalized_signature = (signature or "").strip()
    if not normalized_signature:
        return public_url
    return f"{normalized_signature}\n{public_url}"


def generate_qr_code_base64(payload: str, target_size_mm: int = QR_CODE_SIZE_MM) -> str:
    """Generate a PNG QR code and return it as base64."""
    qr = qrcode.QRCode(border=4, box_size=10)
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    target_pixels = max(1, round((target_size_mm / 25.4) * QR_CODE_RENDER_DPI))
    image = image.resize((target_pixels, target_pixels), Image.Resampling.NEAREST)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
