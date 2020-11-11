from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://site.db'
db = SQLAlchemy(app)


@app.route("/")
def home():
    return "hello"



class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(20), unique=True, nullable=False)
    on_off = db.Column(db.String(5), default='off')
    color = db.Column(db.String(20), default='white')
    brightness = db.Column(db.String(10),default='100')
    animation = db.Column(db.String(20), default=None)















if __name__ == "__main__":
    app.run(debug=True)
