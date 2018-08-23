import os
import requests
from lxml import html
import scrapy
from flask import Flask, render_template, send_from_directory, request
from jinja2 import Template

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')
    # return r.headers.get('server')
    
@app.route('/', methods=['POST'])
def my_form_post():
    list_link = []
    list_cdn = []
    list_result = []
    list_server = ['Google Tag Manager (scaffolding)', 'ss1', None, 'nginx', 'Golfe2']
    text = request.form['link']
    page = requests.get(text)
    tree = html.fromstring(page.content)
    link_resources = tree.xpath('//@src')
    i = 0
    for y in link_resources:
        if (".jpg" in y or ".png" in y or ".js" in y):
            bool_http = y.find('http://') >= 0
            bool_https = y.find('https://') >= 0
            bool_htm = y.find('.htm') < 0
            if (bool_https == True or bool_http == True):
                list_link.append(y)
            i += 1
            if i == 11:
                break
    for z in list_link:
        z_page = requests.get(z)
        z_tree = z_page.headers.get('server')
        list_cdn.append(z_tree)
    list_cdn = list(set(list_cdn))
    for a in list_cdn:
        if a not in list_server:
            list_result.append(a)
    # return render_template('index.html', check=list_result)
    if len(list_result) == 0:
        return render_template('index.html', check=['Non-CDN'])
    else:
        return render_template('index.html', check=list_result)
    # result = r.headers.get('server')
    # if int(result.find('nginx')) < 0:
    #     return render_template('index.html', check=result, link=text)
    # else:
    #     return render_template('index.html', check='None', link=text)
    

@app.route('/static/<path:filename>')
def public_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
   app.run()