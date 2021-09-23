from flask import Blueprint, render_template
from flask import current_app as app

from flask_paginate import Pagination, get_page_args

from core.decorators import login_required
from core.utils.utils import misc
from core.utils.experiment import experiment

experiment_blueprint = Blueprint('experiment', __name__)


@experiment_blueprint.route('/')
@experiment_blueprint.route('/list')
# @login_required(role='user')
def list_experiments():
    """List all the experiments."""
    subfolders = misc.list_subfolders("data/*/")
    experiment_folders = misc.list_experiments(subfolders)
    experiments = list()
    for exp in experiment_folders:
        try:
            date = misc.timestamp_to_date(int(exp) / 1000)
            exp_class = experiment.experiment(new_experiment=False, ts=exp)

            if "label" in exp_class.metadata:
                label = exp_class.metadata["label"]
            else:
                label = None

            exp_dict = {"date": date, "ts": exp, "label": label}
            experiments.append(exp_dict)
        except:
            app.logger.info("Skipped {exp}".format(exp=exp))

    experiments.reverse()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(experiments)
    pagination_experiments = experiments[offset:offset+per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('experiments.html',
                           user=experiments,
                           pagination_experiments=pagination_experiments,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
