from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # import & register blueprints
    from scanner.routes import scanner_bp
    from ai.routes import ai_bp

    app.register_blueprint(scanner_bp)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=9697, debug=True)
