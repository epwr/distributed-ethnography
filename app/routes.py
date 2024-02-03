import logging

from flask import Flask, render_template, request, redirect
from flask_htmx import HTMX
import jinja_partials

from .flask_utils import htmx_or_json
from .data_service import DataService, Sqlite3Driver
from .config import settings
from app.data_service.models import Survey

logging.info(f"Running with settings: {settings}")

app = Flask(__name__)
htmx = HTMX(app)
jinja_partials.register_extensions(app)


@app.before_request
def create_data_service():
    app.data_service = DataService(
        Sqlite3Driver(
            db_file=settings.sqlite_file
        )
    )

@app.route('/')
def get_index_page():
    return render_template('index.html')

@app.route('/admin')
def get_admin_page():
    return render_template('admin.html')


@app.route('/surveys')
@htmx_or_json(template="molecules/survey_list.html")
def get_open_surveys():

    surveys = app.data_service.get_open_surveys()

    return {
        'surveys': surveys
    }

@app.route('/surveys/new', methods=["POST"])
def create_survey():

    data = request.json

    try:
        new_survey = Survey(
            name=data['name'],
            is_open=data['is_open'],
        )
    except KeyError:
        return {
            'error': 'Request should contain "name" and "is_open" fields.'
        }, 400

    data_service: DataService = app.data_service
    data_service.insert_survey(new_survey)

    return {
        'survey_uid': str(new_survey.uid)
    }
