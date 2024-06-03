from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = "6b5ee3ccd68845fb7a10663397b4bcee625d50e8da65109ba9874d998a6d9a02"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inksphere.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

CORS(app)
bcrypt = Bcrypt(app)
api = Api(app)

