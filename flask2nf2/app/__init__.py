from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import fdb
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint
from flask_login import LoginManager
# from flask_mail import Mail
# mail = Mail()
app = Flask(__name__)
# mail.init_app(app)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

# cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:4200"}})

# @app.route('/foo', methods=['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])



# migrate = Migrate(app, db)

# ma = Marshmallow(app)

auth = HTTPBasicAuth()

from .authmain import authmain as authmain_blueprint
app.register_blueprint(authmain_blueprint)


from .main import main as main_blueprint
app.register_blueprint(main_blueprint)


login_manager = LoginManager()
login_manager.login_view = 'authmain.login'
login_manager.init_app(app)
from app.models import User
@login_manager.user_loader
def load_user(user_emailnet):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return db.session.query(User).filter_by(emailnet=user_emailnet).first()

from app import main, authmain, models

# mail = Mail(app)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'zakilebbah@gmail.com'
# app.config['MAIL_PASSWORD'] = "kbqxckowzgfotzmm"
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)
