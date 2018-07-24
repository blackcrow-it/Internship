from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/quanghung/Desktop/Internship/API-Restful/api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = 'example'
    email = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(10))

    def __init__(self, email, name, date):
        self.email = email
        self.name = name
        self.date = date

@app.route('/user', methods=["GET", "POST"])
def create():
    request_json = request.get_json()
    if request.method == "GET":
        user = users.query.all()
        print user
        return "GET request"
    elif request.method == "POST":
        exists = users.query.filter_by(email=request_json.get('email')).scalar() is not None
        if exists == True:
            return "Email Exists"
        else:
            user = users(request_json.get('email'), request_json.get('name'), request_json.get('date'))
            db.session.add(user)
            db.session.commit()
            return "Create: " + request_json.get('email')

@app.route('/user/<string:email_user>', methods=["GET", "PUT"])
def handle(email_user):
    if request.method == "GET":
        exists = users.query.filter_by(email=email_user).scalar() is not None
        user = users.query.filter_by(email=email_user).first()
        if exists == True:
            data = {
                "email" : user.email,
                "name" : user.name,
                "date" : user.date
            }
            return jsonify(data)
        else:
            return "User Not Exists"
    elif request.method == "PUT":
        request_json = request.get_json()
        exists = users.query.filter_by(email=email_user).scalar() is not None
        if exists == True:
            user = users.query.filter_by(email=email_user).first()
            user.name = request_json.get('name')
            db.session.commit()
            user.date = request_json.get("date")
            db.session.commit()
            data = {
                "email" : user.email,
                "name" : user.name,
                "date" : user.date
            }
            return jsonify(data)
        else:
            return "User Not Exists"

if __name__ == '__main__':
    app.run(debug=True) 


