import psycopg2
from config import settings
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class QuizDB(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings['host'],
            dbname=settings['dbname'],
            user=settings['user'],
            password=settings['password']
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_question(self, section, number):
        if not self.cursor:
            return None

        self.cursor.execute(
            "SELECT\n"
            "   id,\n"
            "   description\n"
            "FROM\n"
            "   questions\n"
            "WHERE\n"
            "   section = %(section)s\n"
            "   AND number = %(number)s\n",
            {
                'section': section,
                'number': number
            }
        )

        question = self.cursor.fetchone()
        if question is None:
            return None

        self.cursor.execute(
            "SELECT\n"
            "   choices.key,\n"
            "   choices.description,\n"
            "   not answers.qid IS NULL AS is_correct\n"
            "FROM\n"
            "   choices\n"
            "   LEFT JOIN answers\n"
            "       ON answers.qid = choices.qid\n"
            "       AND answers.key = choices.key\n"
            "WHERE\n"
            "   choices.qid = %(question_id)s\n",
            {
                'question_id': question[0]
            }
        )

        choices = self.cursor.fetchall()

        print choices[1][2]
        return {
            'question': u'{}'.format(question[1]),
            'choices': [
                {
                    'key': u'{}'.format(choice[0]),
                    'text': u'{}'.format(choice[1]),
                    'correct': bool(choice[2])
                }
                for choice in choices
            ]
        }


