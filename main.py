"""
This is an app to control the settings of
various IOT devices
"""
# Import Modules
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application = app
db = SQLAlchemy(app)

migrate = Migrate(app,db)
@app.route("/")
def home():
    return "hello"

@app.route("/<item>/power/<state>")
def power(state, item):
    device = Device.query.filter_by(device_name=item)[0]
    if state == 'off':
        device.on_off = 'off'
        db.session.commit()
        return 'ok'
    elif state == 'on':
        device.on_off = 'on'
        device.change_color = "1"
        db.session.commit()
        return 'ok'
    else:
        return 'ok'

@app.route('/<item>/brightness/<level>')
def brightness(item, level):
    device = Device.query.filter_by(device_name=item)[0]
    try:
        int(level)
        device.brightness = level
        db.session.commit()
        return 'ok'
    except:
        return 'ok'

@app.route('/<item>/color/<color>')
def color(item, color):
    device = Device.query.filter_by(device_name=item)[0]
    device.color = color
    device.change_color = "1"
    device.animation = 'none'
    db.session.commit()
    return 'ok'

@app.route('/<item>/animation/<animation>')
def animation(item, animation):
    device = Device.query.filter_by(device_name=item)[0]
    device.animation = animation
    if animation == "none":
        device.change_color == "1"
    db.session.commit()
    return 'ok'

@app.route('/<item>/settings')
def settings(item):
    device = Device.query.filter_by(device_name=item)[0]
    return render_template('settings.html',device=device)

@app.route('/<item>/get_settings')
def get_settings(item):
    device = Device.query.filter_by(device_name=item)[0]
    del device.__dict__['_sa_instance_state']
    j = jsonify(dict(device.__dict__))
    return j
@app.route('/<item>/change_color/<var>')
def change_col(item,var):
    device = Device.query.filter_by(device_name=item)[0]
    device.change_color = var
    db.session.commit()
    return 'ok'
@app.route('/<item>/saturation/<var>')
def saturation(item, var):
    device = Device.query.filter_by(device_name=item)[0]
    device.saturation = var
    db.session.commit()
    return "ok"

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(20), unique=True, nullable=False)
    on_off = db.Column(db.String(5), default='off', nullable=False)
    color = db.Column(db.String(20), default='white', nullable=False)
    saturation = db.Column(db.String(20), default='1')
    brightness = db.Column(db.String(10),default='100',nullable=False)
    animation = db.Column(db.String(20), default=None)
    change_color = db.Column(db.String(10), default="0")

    def __repr__(self):
        return '<Device %r>' % self.device_name












#if __name__ == "__main__":
 #   app.run(debug=True)
