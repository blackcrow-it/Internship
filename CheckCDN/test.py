import os
import requests
import scrapy
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')
    # return r.headers.get('server')
    
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['link']
    r = requests.get(text)
    result = r.headers.get('server')
    if int(result.find('nginx')) < 0:
        return render_template('index.html', check=result, link=text)
    else:
        return render_template('index.html', check='None', link=text)


@app.route('/static/<path:filename>')
def public_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
   app.run()