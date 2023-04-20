from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def home_page():
    """Creates the homepages"""

    session["responses"] = []

    return render_template("survey_start.html",title=survey.title, instructions=survey.instructions)

@app.post("/begin")
def start_survey():
    """Starts the given survey"""

    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def question_page(question_number):
    """Loads the page for the current question"""

    current_sesh = session["responses"]

    if question_number > len(current_sesh):
        flash("You are out of bounds")
        return redirect(f"/questions/{len(current_sesh)}")

    question = survey.questions[question_number]

    return render_template("question.html", question = question, question_number=question_number)

@app.post("/answer")
def submit_answer():
    """checks for answer, if answer, continue to next question"""

    current_sesh = session["responses"]
    answer = request.form["answer"]
    if answer:
        current_sesh.append(answer)
        session["responses"] = current_sesh
        if len(current_sesh) >= len(survey.questions):
            return redirect("/completion")
    return redirect(f"/questions/{len(current_sesh)}")

@app.get("/completion")
def completion():
    """Sends user to survery completion page"""

    return render_template("completion.html", responses=session["responses"], questions=survey.questions)



