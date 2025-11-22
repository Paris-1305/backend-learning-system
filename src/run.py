from flask import Flask
from api.lesson_routes import lesson_bp

app = Flask(__name__)
app.register_blueprint(lesson_bp)

if __name__ == "__main__":
    app.run(debug=True)
