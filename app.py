from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.get("/")
def home_page():
    """Creates the homepages"""

    return render_template("survey_start.html",title=survey.title, instructions=survey.instructions)

@app.post("/begin")
def start_survey():
    """Starts the given survey"""

    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def question_page(question_number):
    """Loads the page for the current question"""

    current_question = survey.questions[question_number]

    return render_template("question.html", question = current_question, qestion_number=question_number)

@app.post("/answer/<int:question_number>")
def submit_answer(question_number):

    answer = request.form.get("answer")

    if answer:
        RESPONSES.append(answer)
        question_number += 1
        if question_number == len(survey.questions):
            redirect("/completion")
        else:
            redirect(f"/questions/{question_number}")



