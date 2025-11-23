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

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from .routes.course_routes import course_bp
from .routes.lesson_routes import lesson_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # -------------------------------------------------
    # ENABLE GLOBAL CORS (correct, no conflicts)
    # -------------------------------------------------
    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "http://localhost:5173",
            "https://learningfy.netlify.app"
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "x-api-key"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # -------------------------------------------------
    # HANDLE OPTIONS REQUESTS (REQUIRED ON RENDER)
    # -------------------------------------------------
    @app.route("/api/<path:path>", methods=["OPTIONS"])
    def api_options(path):
        return ("", 200)

    # -------------------------------------------------
    # ENSURE ALL RESPONSES INCLUDE CORS HEADERS
    # -------------------------------------------------
    @app.after_request
    def add_cors_headers(response):
        allowed_origins = [
            "http://localhost:5173",
            "https://learningfy.netlify.app"
        ]
        origin = response.headers.get("Access-Control-Allow-Origin")
        # Only override if CORS didn't add it yet
        if not origin:
            response.headers["Access-Control-Allow-Origin"] = "https://learningfy.netlify.app"
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

    # Docs
    @app.route('/docs')
    def docs():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Learnify API Docs</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css" />
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
            <script>
                const ui = SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout"
                });
            </script>
        </body>
        </html>
        '''

    # -------------------------------------------------
    # Register API routes
    # -------------------------------------------------
    app.register_blueprint(course_bp, url_prefix="/api")
    app.register_blueprint(lesson_bp, url_prefix="/api")

    return app
