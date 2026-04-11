from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any, Dict, Optional

SECRET_KEY = secrets.token_bytes(32)


def hash_password(password: str, salt: Optional[bytes] = None) -> str:
    if salt is None:
        salt = secrets.token_bytes(16)
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 150_000)
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 150_000)
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_token(payload: Dict[str, Any], expires_in_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "TTR"}
    now = int(time.time())
    body = dict(payload)
    body["iat"] = now
    body["exp"] = now + expires_in_seconds
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body_b64 = _b64url_encode(json.dumps(body, separators=(",", ":")).encode("utf-8"))
    message = f"{header_b64}.{body_b64}".encode("utf-8")
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
    return f"{header_b64}.{body_b64}.{_b64url_encode(signature)}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        header_b64, body_b64, sig_b64 = token.split(".", 2)
        message = f"{header_b64}.{body_b64}".encode("utf-8")
        expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, _b64url_decode(sig_b64)):
            return None
        payload = json.loads(_b64url_decode(body_b64))
        if int(payload.get("exp", 0)) < int(time.time()):
            return None
        return payload
    except Exception:
        return None
