# simple flask to serve report.html
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Path: templates/report.html
# to run the server, run the following command:
# python server.py