from api import create_app
import os

from api.config import Config

app = create_app(Config)


if __name__ == '__main__':
    app.run(host=os.getenv('HOST', "0.0.0.0"), port=os.getenv('PORT', 3000),
            debug=os.getenv('FLASK_DEBUG', False))