from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from .routes.course_routes import course_bp
from .routes.lesson_routes import lesson_bp


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # Enable CORS for all routes
    #CORS(app)
  # Enable CORS for all routes FROM your frontend
    #CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    CORS(app, resources={r"/api/*": {"origins": "https://learningfy.netlify.app"}})
    # Serve OpenAPI spec
    @app.route('/openapi.json')
    def serve_openapi():
        static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static')
        return send_from_directory(static_dir, 'openapi.json')

    # Serve docs page
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

    # Register blueprints
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(lesson_bp, url_prefix='/api')

    return app