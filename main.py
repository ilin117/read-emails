import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from email_auto_reader import mark_emails_as_read

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR, static_url_path='/static')
CORS(app=app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/mark-read', methods=['POST'])
def mark_read():
    result = mark_emails_as_read()
    return jsonify(result)


if __name__ == '__main__':
    # debug=False for safety; use a production WSGI server for real deployments
    app.run(debug=False, port=7000)
