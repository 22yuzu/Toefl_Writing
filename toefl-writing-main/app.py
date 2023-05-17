
from flask import Flask, render_template, request, jsonify, session, abort
from flask_cors import CORS 
import openai
import os
from dotenv import load_dotenv
from gpt import generate_question, score_answer

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI key
openai.api_key = os.getenv('OPENAI_KEY')

# secret key for session
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            question = generate_question()
        except Exception as e:
            abort(500, description="Error generating question")
        session['question'] = question  # Save question in session
        return render_template('index.html', question=question)
    else:
        return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
    data = request.get_json() 
    answer = data.get('answer')  
    if not answer or not isinstance(answer, str):
        abort(400, description="Invalid answer data")
    question = session.get('question')  # Get question from session
    try:
        # Call the score_answer function to perform the scoring
        score, feedback, sample_answer = score_answer(answer, question)
    except Exception as e:
        abort(500, description="Error scoring answer")

    # Save results in session
    session['score'] = score
    session['feedback'] = feedback
    session['sample_answer'] = sample_answer

    return jsonify({'status': 'success'})

@app.route('/results', methods=['GET'])
def results():
    score = session.get('score')
    feedback = session.get('feedback')
    sample_answer = session.get('sample_answer')
    # Clear session
    session.clear()
    return render_template('results.html', score=score, feedback=feedback, sample_answer=sample_answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
