import os
import requests
from lxml import html
import scrapy
from flask import Flask, render_template, send_from_directory, request
from jinja2 import Template
import test
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')
    # return r.headers.get('server')
    
@app.route('/', methods=['POST'])

def my_form_post():
    list_link_img = []
    list_link_css_js = []
    list_cdn_img = []
    list_cdn_css_js = []
    list_result_img = []
    list_result_css_js = []
    list_server = ['Google Tag Manager (scaffolding)', 'ss1', None, 'nginx', 'nginx/1.10.3 (Ubuntu)', 'Golfe2', 'Skimlinks V9.0', 'nginx/1.13.6', 'AmazonS3', 'Apache', 'imgix-fe', 'sffe', 'LiteSpeed', 'ESF']
    text = request.form['link']
    try:
        with eventlet.timeout.Timeout(30):
            response = requests.get('{}'.format(text))
        page = requests.get(text)
        tree = html.fromstring(page.content)
        link_resources = tree.xpath('//@src')
        test.get_link(".jpg", ".png", link_resources, list_link_img)
        test.get_link(".css", ".js", link_resources, list_link_css_js)
        test.get_cdn(list_link_img, list_cdn_img)
        test.get_cdn(list_link_css_js, list_cdn_css_js)
        list_cdn_img = list(set(list_cdn_img))
        list_cdn_css_js = list(set(list_cdn_css_js))
        # print list_cdn_css_js
        test.get_result(list_cdn_img, list_result_img, list_server)
        test.get_result(list_cdn_css_js, list_result_css_js, list_server)
        list_result_css_js = test.format_cdn(list_result_css_js)
        if len(list_result_img) == 0 and len(list_result_css_js) == 0:
            return render_template('index.html', check_img=['<Non-CDN>'], check_css_js=['<Non-CDN>'])
        elif len(list_result_img) != 0 and len(list_result_css_js) == 0:
            return render_template('index.html', check_img=list_result_img, check_css_js=['<Non-CDN>'])
        elif len(list_result_img) == 0 and len(list_result_css_js) != 0:
            return render_template('index.html', check_img=['<Non-CDN>'], check_css_js=list_result_css_js)
        else:
            return render_template('index.html', check_img=list_result_img, check_css_js=list_result_css_js)
        print "Ok -", text
    except requests.exceptions.ReadTimeout:
        print "READ time out - ", text
        return render_template('index.html', check_error="Not Found Site")
    except requests.exceptions.ConnectionError:
        print "CONNECT ERROR -", text
        return render_template('index.html', check_error="Not Found Site")
    except eventlet.timeout.Timeout, e:
        print "TOTAL TIMEOUT -", text
        return render_template('index.html', check_error="Time Out")
    except requests.exceptions.RequestException, e:
        print "OTHER REQUESTS EXCEPTION -", text, e
        return render_template('index.html', check_error="Not Found Site")
    
    

@app.route('/static/<path:filename>')
def public_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
   app.run()