from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from email_auto_reader import mark_emails_as_read

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app=app)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/style.css')
def style():
    return send_from_directory(app.static_folder, 'style.css')


@app.route('/script.js')
def script():
    return send_from_directory(app.static_folder, 'script.js')


@app.route('/api/mark-read', methods=['POST'])
def mark_read():
    result = mark_emails_as_read()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=7000)
