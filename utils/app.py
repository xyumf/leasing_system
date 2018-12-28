from flask import Flask
from app.user_views import user_blue
from app.home_views import home_blue
from app.order_views import order_blue
from app.models import db
from utils.settings import STATIC_PATH, TEMPLATE_PATH
from utils.config import Conf


def create_app():
    app = Flask(__name__,static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH)
    app.config.from_object(Conf)
    app.register_blueprint(blueprint=user_blue, url_prefix='/user')
    app.register_blueprint(blueprint=home_blue, url_prefix='/home')
    app.register_blueprint(blueprint=order_blue, url_prefix='/order')
    db.init_app(app)

    return app