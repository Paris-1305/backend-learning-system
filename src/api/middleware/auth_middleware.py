from functools import wraps
from flask import request, jsonify
from src.config.config import Config

def require_api_key(f):
    """
    Middleware decorator to protect routes using API Key authentication.
    Expects header: Authorization: Bearer <API_KEY>
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "UNAUTHORIZED",
                "message": "Authorization header is missing. Use format: Bearer <API_KEY>"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "error": "UNAUTHORIZED",
                "message": "Invalid Authorization format. Use format: Bearer <API_KEY>"
            }), 401

        api_key = auth_header.split(" ")[1].strip()

        if api_key not in Config.VALID_API_KEYS:
            return jsonify({
                "error": "UNAUTHORIZED",
                "message": "Invalid API Key provided."
            }), 401

        # Optional: log the key for debugging
        print("Received key:", api_key)
        print("Allowed keys:", Config.VALID_API_KEYS)

        return f(*args, **kwargs)

    return decorated

