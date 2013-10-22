from urlparse import urlparse
from flask import Flask, render_template, request
import sqlite3
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

def connect():
    return sqlite3.connect(app.config['db_path'])

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
    with open('db.path') as dbp:
        app.config['db_path'] = dbp.readline().strip()
    app.run()
