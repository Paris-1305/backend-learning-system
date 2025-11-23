# from flask import Flask, send_from_directory
# from flask_cors import CORS
# import os
# from .routes.course_routes import course_bp
# from .routes.lesson_routes import lesson_bp


# def create_app():
#     """Application factory pattern"""
#     app = Flask(__name__)

#     # Enable CORS for all routes
#     #CORS(app)
#     #CORS(app, resources={r"/api/*": {"origins": "https://learningfy.netlify.app"}})
#     CORS(app, resources={
#     r"/*": {
#         "origins": [
#             "http://localhost:5173",
#             "https://learningfy.netlify.app"
#         ],
#         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization", "x-api-key"],
#         "supports_credentials": True
#     }
# })
   


    
#     # Serve OpenAPI spec
#     @app.route('/openapi.json')
#     def serve_openapi():
#         static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static')
#         return send_from_directory(static_dir, 'openapi.json')

#     # Serve docs page
#     @app.route('/docs')
#     def docs():
#         return '''
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Learnify API Docs</title>
#             <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css" />
#         </head>
#         <body>
#             <div id="swagger-ui"></div>
#             <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
#             <script>
#                 const ui = SwaggerUIBundle({
#                     url: '/openapi.json',
#                     dom_id: '#swagger-ui',
#                     presets: [
#                         SwaggerUIBundle.presets.apis,
#                         SwaggerUIBundle.SwaggerUIStandalonePreset
#                     ],
#                     layout: "BaseLayout"
#                 });
#             </script>
#         </body>
#         </html>
#         '''

#     # Register blueprints
#     app.register_blueprint(course_bp, url_prefix='/api')
#     app.register_blueprint(lesson_bp, url_prefix='/api')

#     return app
import os
import logging
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from .routes.course_routes import course_bp
from .routes.lesson_routes import lesson_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # -------------------------------------------------
    # ENABLE LOGGER (prints all requests)
    # -------------------------------------------------
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("learnify-api")

    @app.before_request
    def log_request():
        # Log all incoming requests to help debug the 404/OPTIONS issue
        logger.info(f"➡️ {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")

    # -------------------------------------------------
    # ENABLE GLOBAL CORS (WIDENED TO '/*' for diagnosis)
    # -------------------------------------------------
    # IMPORTANT: Changing r"/api/*" to r"/*" allows the CORS middleware
    # to handle the OPTIONS request for paths like /courses (which was failing 
    # with a 404 because Flask couldn't find a route). 
    CORS(
        app,
        resources={r"/*": {  # <--- Changed from r"/api/*" to r"/*"
            "origins": [
                "http://localhost:5173",
                "https://learningfy.netlify.app"
            ],
            "supports_credentials": True,
            "allow_headers": ["Content-Type", "Authorization", "x-api-key"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        }},
    )

    # -------------------------------------------------
    # HANDLE OPTIONS REQUESTS (Redundant now, but kept for clarity)
    # -------------------------------------------------
    @app.route("/api/<path:path>", methods=["OPTIONS"])
    @app.route("/<path:path>", methods=["OPTIONS"]) # Added a catch-all OPTIONS handler
    def api_options(path=None):
        # The CORS middleware should handle the headers, this just ensures a 200 OK response
        # is returned for any OPTIONS request that might otherwise hit a 404.
        return ("", 200)

    # -------------------------------------------------
    # Force-CORS on all responses (fix Render bug) - Remove if no longer needed
    # -------------------------------------------------
    @app.after_request
    def add_cors_headers(response):
        # Since CORS is now configured globally, this section is mostly redundant
        # but kept to ensure maximum compatibility.
        origin = request.headers.get("Origin")
        allowed = [
            "https://learningfy.netlify.app",
            "http://localhost:5173"
        ]
        
        # Only set Access-Control-Allow-Origin if the Origin is in our allowed list
        if origin in allowed:
            response.headers["Access-Control-Allow-Origin"] = origin
        
        # Ensure other headers are always present on all responses
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, x-api-key"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    # -------------------------------------------------
    # Serve OpenAPI Spec
    # -------------------------------------------------
    @app.route('/openapi.json')
    def serve_openapi():
        static_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'static'
        )
        return send_from_directory(static_dir, 'openapi.json')

    # -------------------------------------------------
    # Render Swagger Docs
    # -------------------------------------------------
    @app.route('/docs')
    def docs():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Learnify API Docs</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
                SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui'
                });
            </script>
        </body>
        </html>
        '''

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------
    app.register_blueprint(course_bp, url_prefix="/api")
    app.register_blueprint(lesson_bp, url_prefix="/api")

    return app