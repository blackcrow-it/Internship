from flask import Flask, request
from redis import Redis
redis = Redis(host='127.0.0.1', port=6379)
app = Flask(__name__, static_folder='')

@app.route("/")
def main():
    user_agent = request.headers.get('User-Agent')
    redis.pfadd('user', user_agent)
    count_ua = redis.pfcount('user')
    print 'Count user-agent: {}'.format(count_ua)
    print user_agent
    return app.send_static_file('template/index.html')
    # return 'Hello'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)