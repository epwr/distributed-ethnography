import logging

from flask import Flask, render_template
from flask_htmx import HTMX
import jinja_partials

from .flask_utils import htmx_partial
from .data_service import DataService
from .data_service.sqlite3 import Sqlite3Driver
from .config import settings

logging.info(f"Running with settings: {settings}")

app = Flask(__name__)
htmx = HTMX(app)
jinja_partials.register_extensions(app)


data_service = DataService(
    Sqlite3Driver(
        db_file=settings.sqlite_file
    )
)


@app.route('/')
def get_index_page():
    return render_template('index.html')


@app.route('/surveys')
@htmx_partial(template="molecules/survey_list.html", redirection="/")
def get_test_values():

    surveys = data_service.get_open_surveys()
    
    return {
        'surveys': surveys
    }
