import logging
from typing import Dict, Any
from uuid import UUID

from flask import Flask, render_template, request, abort
import jinja_partials  # type: ignore

from .flask_utils import htmx_endpoint
from .data_service import DataService, Sqlite3Driver
from .config import settings
from app.models import Survey

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
    data_service: DataService = app.data_service  # type: ignore[attr-defined]
    surveys = data_service.get_open_surveys()

    return {"surveys": surveys}


@app.route("/surveys/<uid>")
def get_survey(uid: str) -> str:
    data_service: DataService = app.data_service  # type: ignore[attr-defined]
    survey_uid = UUID(uid)
    survey = data_service.get_survey_if_open(survey_uid)

    if survey is None:
        abort(404, "Could not find a survey with that UUID.")

    return render_template("survey.html", survey=survey)


@app.route("/surveys/new")
def get_create_survey_page() -> str:
    return render_template("create_survey.html")


@app.route("/surveys/new", methods=["POST"])
@htmx_endpoint(template="molecules/survey_submitted.html")
def create_survey() -> dict[str, Any]:
    data: dict[str, Any] = request.form

    try:
        for key in data.keys():
            if key not in ("name", "is_open"):
                raise KeyError(f"Received unexpected key '{key}'")
        new_survey = Survey(
            name=data["name"],
            is_open=data.get("is_open", False),
        )
    except KeyError:
        logging.error(f"/surveys/new received a submission of the following: {data}")
        abort(400, 'Survey submission should contain "name" and "is_open" fields.')

    data_service: DataService = app.data_service  # type: ignore[attr-defined]
    data_service.insert_survey(new_survey)

    return {"survey_uid": str(new_survey.uid)}
