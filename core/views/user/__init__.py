from flask import Blueprint, render_template
from core.decorators import login_required

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/dashboard')
@login_required(role='user')
def dashboard():
	return render_template('index.html')
