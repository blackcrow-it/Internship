from flask import Flask, request, render_template
from redis import Redis
from time import gmtime, strftime
redis = Redis(host='127.0.0.1', port=6379)
app = Flask(__name__)

@app.route("/")
def main():
    user_agent = request.headers.get('User-Agent')
    time_now = strftime("%Y-%m-%d", gmtime())
    redis.pfadd(time_now, user_agent)
    count_ua = redis.pfcount('user')
    print time_now
    print 'Count user-agent: {}'.format(count_ua)
    # print user_agent
    return render_template('/index.html')
    # return 'Hello'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)