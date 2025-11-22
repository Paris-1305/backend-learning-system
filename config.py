import os


class Config:
    """Flask application configuration"""

    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'learnify.db')

    # API settings
    VALID_API_KEYS = [
        'test-api-key-12345'
    ]