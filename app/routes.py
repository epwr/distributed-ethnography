import logging
from typing import Dict, Any

from flask import Flask, render_template, request, abort
import jinja_partials  # type: ignore

from .flask_utils import htmx_endpoint
from .data_service import DataService, Sqlite3Driver
from .config import settings
from app.data_service.models import Survey

logging.info(f"Running with settings: {settings}")

app = Flask(__name__)
jinja_partials.register_extensions(app)


@app.before_request
def create_data_service() -> None:
    app.data_service = DataService(  # type: ignore[attr-defined]
        Sqlite3Driver(db_file=settings.sqlite_file)
    )


@app.route("/")
def get_index_page() -> str:
    return render_template("index.html")


@app.route("/admin")
def get_admin_page() -> str:
    return render_template("admin.html")


@app.route("/surveys")
@htmx_endpoint(template="molecules/survey_list.html")
def get_open_surveys() -> Dict[str, Any]:
    surveys = app.data_service.get_open_surveys()  # type: ignore[attr-defined]

    return {"surveys": surveys}


@app.route("/surveys/new", methods=["POST"])
def create_survey() -> dict[str, Any]:
    data: dict[str, Any] = request.json  # type: ignore

    try:
        new_survey = Survey(
            name=data["name"],
            is_open=data["is_open"],
        )
    except KeyError:
        abort(400, 'Request should contain "name" and "is_open" fields.')

    data_service: DataService = app.data_service  # type: ignore[attr-defined]
    data_service.insert_survey(new_survey)

    return {"survey_uid": str(new_survey.uid)}
