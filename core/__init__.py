from flask import Flask, render_template

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import rq_dashboard

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_object(rq_dashboard.default_settings)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from core.views.auth import auth_blueprint  # noqa
from core.views.user import user_blueprint  # noqa
from core.views.admin import admin_blueprint  # noqa
from core.views.system import system_blueprint  # noqa
from core.views.video import video_blueprint  # noqa
from core.views.experiments import experiment_blueprint  # noqa


app.register_blueprint(experiment_blueprint, url_prefix='/experiment')
app.register_blueprint(video_blueprint, url_prefix='/video')
app.register_blueprint(system_blueprint, url_prefix='/system')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(rq_dashboard.blueprint, url_prefix='/monitor')


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(400)
def error_400(e):
    return render_template("error/400.html")


@app.errorhandler(401)
def error_401(e):
    return render_template("error/401.html")


@app.errorhandler(403)
def error_403(e):
    return render_template("error/403.html")


@app.errorhandler(404)
def error_404(e):
    return render_template("error/404.html")


@app.errorhandler(408)
def error_408(e):
    return render_template("error/408.html")


@app.errorhandler(410)
def error_410(e):
    return render_template("error/410.html")
