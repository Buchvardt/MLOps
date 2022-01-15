from flask import Flask, render_template, request, flash, url_for, redirect
import logging
from config import config
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'

app_name = config["app_name"]

@app.route('/')
def index():

   
    return render_template('index.html', app_name=app_name)

@app.route('/create', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':

        title = request.form['title']

        content = request.form['content']

        if len(title) == 0:

            flash('Title is required!')

        else:

            resp = requests.post(config["rest_api_endpoint"], json={"title": title, "content": content})

            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)