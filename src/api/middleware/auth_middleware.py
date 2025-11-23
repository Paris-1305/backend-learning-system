# from functools import wraps
# from flask import request, jsonify
# from src.config.config import Config

# def require_api_key(f):
#     """
#     Middleware decorator to protect routes using API Key authentication.
#     Expects header: Authorization: Bearer <API_KEY>
#     """

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Authorization header is missing. Use format: Bearer <API_KEY>"
#             }), 401

#         if not auth_header.startswith("Bearer "):
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Invalid Authorization format. Use format: Bearer <API_KEY>"
#             }), 401

#         api_key = auth_header.split(" ")[1].strip()

#         if api_key not in Config.VALID_API_KEYS:
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Invalid API Key provided."
#             }), 401

#         # Optional: log the key for debugging
#         print("Received key:", api_key)
#         print("Allowed keys:", Config.VALID_API_KEYS)

#         return f(*args, **kwargs)

#     return decorated

from functools import wraps
from flask import request, jsonify
from src.config.config import Config

# def require_api_key(f):
#     """
#     Middleware decorator to protect routes using API Key authentication.
#     Expects header: Authorization: Bearer <API_KEY>
#     """

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         # Get the Authorization header
#         auth_header = request.headers.get("Authorization")

#         # Check if header exists
#         if not auth_header:
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Authorization header is missing. Use format: Bearer <API_KEY>"
#             }), 401

#         # Check if header is in the correct format
#         if not auth_header.startswith("Bearer "):
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Invalid Authorization format. Use format: Bearer <API_KEY>"
#             }), 401

#         # Extract API key
#         api_key = auth_header.split(" ")[1].strip()

#         # Validate API key
#         if api_key not in Config.VALID_API_KEYS:
#             return jsonify({
#                 "error": "UNAUTHORIZED",
#                 "message": "Invalid API Key provided."
#             }), 401

#         # Optional: logging for debugging
#         print(f"[AUTH] API key validated: {api_key}")

#         # Proceed to the actual route function
#         return f(*args, **kwargs)

#     return decorated
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "UNAUTHORIZED", "message": "Missing or invalid Authorization header."}), 401
        api_key = auth_header.split(" ")[1].strip()
        if api_key not in Config.VALID_API_KEYS:
            return jsonify({"error": "UNAUTHORIZED", "message": "Invalid API Key."}), 401
        return f(*args, **kwargs)
    return decorated
