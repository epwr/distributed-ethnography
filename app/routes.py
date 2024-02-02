from flask import Flask, render_template, redirect
from flask_htmx import HTMX
import jinja_partials

from .flask_utils import htmx_partial

app = Flask(__name__)
htmx = HTMX(app)
jinja_partials.register_extensions(app)


@app.route('/')
def get_index_page():
    return render_template('index.html')


@app.route('/surveys')
@htmx_partial(template="molecules/survey_list.html", redirection="/")
def get_test_values():
    return {
        'surveys': ['survey1', 'survey2']
    }
