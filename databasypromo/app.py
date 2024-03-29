from urlparse import urlparse
from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.exceptions import BadRequest

WORKING_DIR = os.path.join(os.path.dirname(__file__), '..')
DB_FILE = os.path.join(WORKING_DIR, 'databasypromo.db')
LOG_FILE = os.path.join(WORKING_DIR, 'databasypromo.log')

app = Flask(__name__)
if not app.debug:
    import logging
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

def connect():
    return sqlite3.connect(DB_FILE)

@app.route('/', methods=['GET'])
def promo():
    with connect() as c:
        try:
            referrer = request.environ['HTTP_REFERER']
        except KeyError:
            c.execute("INSERT INTO visit (uri, netloc, path, time) VALUES (NULL, NULL, NULL, DATETIME('now'))")
        else:
            uri = urlparse(referrer)
            c.execute("INSERT INTO visit (uri, netloc, path, time) VALUES (?, ?, ?, DATETIME('now'))",
                (referrer, uri.netloc, uri.path))
    return render_template('promo.html')


@app.route('/', methods=['POST'])
def betaRequest():
    with connect() as c:
        try:
            email = request.values['email']
        except KeyError:
            raise BadRequest
        c.execute("INSERT INTO email (email, time) VALUES (?, DATETIME('now'))", (email,))
    return ''

if __name__ == '__main__':
    app.run()
