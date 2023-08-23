from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey
app=Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


RESPONSES_KEY="responses"


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

@app.route('/')
def home_page():
    ''' Start the servey '''
    session[RESPONSES_KEY] = []
    return render_template('home.html', satisfaction_survey=satisfaction_survey)



@app.route('/answer', methods=['POST'])
def save_answer():
    """Save response and redirect to next question."""

    # get the response choice
    response = request.form['choice']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(response)
    session[RESPONSES_KEY] = responses


    # check if there are more questions
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank_you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank_you')
def thank_you():
    ''' Show when the survey is complete'''
    return render_template('thank_you.html', responses=session[RESPONSES_KEY])


@app.route('/questions/<int:index>')
def questions(index):
    ''' Display current question '''
    responses=session.get(RESPONSES_KEY,[])

    if responses is None:
        return redirect('/')
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank_you')
    
    if len(responses)!=index:
        flash(f"Invalid question id: {index}.")
        return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[index]
    return render_template("questions.html", satisfaction_survey=satisfaction_survey, index=index, question=question)

    # else:
    #     return "Question doesn't exist"    