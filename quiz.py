from flask import Flask
from flask import g
from flask import render_template
from flask import jsonify
from modules.crossdomain import crossdomain

from modules.db import QuizDB

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.quizDB = QuizDB()
    return db


@app.route('/q/<int:section>/<int:number>')
def show_question(section, number):

    response = get_db().get_question(section, number)
    if response is None:
        return 'Question not found'

    return render_template(
        'question.html',
        question=response['question'],
        choices=response['choices'],
        section=section,
        number=number
    )


@app.route('/rest/q/<int:section>/<int:number>')
@crossdomain(origin='*')
def get_question_json(section, number):

    response = get_db().get_question(section, number)
    return jsonify(response)


@app.route("/")
def hello():
    return "Good morning!"


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, '_database'):
        del g.quizDB


if __name__ == "__main__":
    pass
