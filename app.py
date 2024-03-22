from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize responses list
questions_list = [
    "Do you like cats?",
    "Have you ever been to Paris?",
    "What is your annual income?"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_survey', methods=['POST'])
def start_survey():
    session['responses'] = []  # Initialize session variable for responses
    flash('Survey started. Please proceed to the first question.')
    return redirect(url_for('questions', question_number=0))

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    if 'responses' not in session:
        session['responses'] = []

    if len(session['responses']) == len(questions_list):
        return redirect(url_for('survey_complete'))

    if request.method == 'POST':
        response = request.form['response']
        session['responses'].append(response)
        
        next_question_number = question_number + 1
        if next_question_number < len(questions_list):
            return redirect(url_for('questions', question_number=next_question_number))
        else:
            return redirect(url_for('survey_complete'))
    else:
        if question_number < 0 or question_number >= len(questions_list) or question_number != len(session['responses']):
            flash('Invalid question access. Please answer questions sequentially.')
            return redirect(url_for('questions', question_number=len(session['responses'])))
        else:
            question_text = questions_list[question_number]
            return render_template('questions.html', question_text=question_text, question_number=question_number)

@app.route('/survey_complete')
def survey_complete():
    return render_template('survey_complete.html')

if __name__ == '__main__':
    app.run(debug=True)
