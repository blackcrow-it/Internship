from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

def sql_select(email):
    con = sql.connect("/home/quanghung/test.db")
    cur = con.cursor()
    con.row_factory = sql.Row
    cur.execute('select * from user where email = "{}"'.format(email))
    rows = list(cur.fetchall())
    return rows

@app.route('/', methods=["GET", "POST", "DELETE"])
def hello():
    if request.method == "GET":
        # return render_template('/index.html')
        return u'GET requests\n'
    elif request.method == "POST":
        # return render_template('/index.html')
        return "POST requests\n"
    elif request.method == "DELETE":
        # return render_template('/index.html')
        return "DELETE requests\n"

@app.route('/user', methods=["GET", "POST"])
def post():
    con = sql.connect("/home/quanghung/test.db")
    cur = con.cursor()
    if request.method == "GET":
        # return render_template('/index.html')
        return u'GET requests\n'
    elif request.method == "POST":
        request_json = request.get_json()
        print(request.get_json())
        email = request_json.get('email')
        name = request_json.get('name')
        date = request_json.get('date')
        print email
        cur.execute('INSERT INTO user(email, name, date) VALUES ("{}","{}","{}")'.format(email,name,date))
        con.commit()
        con.close()
        return "POST requests\n"
    

@app.route('/user/<string:email>', methods=["GET", "PUT", "DELETE"])
def handle(email):
    con = sql.connect("/home/quanghung/test.db")
    cur = con.cursor()
    if request.method == "GET":
        rows = sql_select(email)
        if len(rows) > 0:
            data = {
                "email": rows[0][0],
                "name": rows[0][1],
                "date": rows[0][2]
            }
            return jsonify(data)
        else:
            return "NO FIND"
    elif request.method == "PUT":
        rows = sql_select(email)
        print len(rows)
        if len(rows) > 0:
            request_json = request.get_json()
            print(request.get_json())
            name = request_json.get('name')
            date = request_json.get('date')
            cur.execute('UPDATE user SET name = "{}", date = "{}" WHERE email = "{}" '.format(name,date,email))
            con.commit()
            con.close()
            return "PUT email: {}".format(email)
        else:
            return "NO FIND"
        return "POST requests\n"

    elif request.method == "DELETE":
        rows = sql_select(email)
        print len(rows)
        if len(rows) > 0:
            cur.execute('DELETE FROM user WHERE email = "{}"'.format(email))
            con.commit()
            con.close()
            return "DELETE email: {}".format(email)
        else:
            return "NO FIND"

if __name__ == '__main__':
    app.run(debug=True) 