import logging
from typing import Dict, Any
from uuid import UUID

from flask import Flask, render_template, request, abort
import jinja_partials  # type: ignore

from .utils import htmx_endpoint, validate_survey_data
from .data_service import DataService, Sqlite3Driver
from .config import settings
from app.models import Survey, TextQuestion

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
    survey = data_service.get_survey_if_open(survey_uid=survey_uid)

    if survey is None:
        abort(404, "Could not find a survey with that UUID.")

    text_questions = data_service.get_text_questions_from_survey(survey_uid=survey_uid)
    dimensional_questions = data_service.get_dimensional_questions_from_survey(
        survey_uid=survey_uid
    )

    return render_template(
        "survey.html",
        survey=survey,
        text_questions=text_questions,
        dimensional_questions=dimensional_questions,
    )


@app.route("/surveys/new")
def get_create_survey_page() -> str:
    return render_template("create_survey.html")


@app.route("/surveys/new", methods=["POST"])
@htmx_endpoint(template="molecules/survey_submitted.html")
def create_survey() -> dict[str, Any]:
    data: dict[str, Any] = request.form
    questions = []

    logging.info(f"/surveys/new request with data {data}")
    print(f"data: {data}")

    error = validate_survey_data(data)
    if error is not None:
        logging.error(f"/surveys/new with {data} could not be validated: {error}")
        abort(400, error)

    new_survey = Survey(
        name=data["name"],
        is_open=data.get(
            "is_open", False
        ),  # False is represented as missing in form data
    )

    questions = [
        (key, value) for key, value in data.items() if key.startswith("question-")
    ]
    questions.sort(key=lambda q: q[0])
    parsed_questions = []

    for index, (question_key, question) in enumerate(questions):
        parsed_questions.append(
            TextQuestion(
                survey_uid=new_survey.uid,
                question=question,
            )
        )

    data_service: DataService = app.data_service  # type: ignore[attr-defined]
    data_service.insert_survey(survey=new_survey)
    for question in parsed_questions:
        data_service.insert_text_question(text_question=question)

    return {"survey_uid": str(new_survey.uid)}
