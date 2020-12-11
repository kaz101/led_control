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
        return redirect(url_for('settings', item=device.device_name))
    elif state == 'on':
        device.on_off = 'on'
        db.session.commit()
        return redirect(url_for('settings', item=device.device_name))
    else:
        return redirect(url_for('settings', item=device.device_name))

@app.route('/<item>/brightness/<level>')
def brightness(item, level):
    device = Device.query.filter_by(device_name=item)[0]
    try:
        int(level)
        device.brightness = level
        db.session.commit()
        return redirect(url_for('settings', item=device.device_name))
    except:
        return redirect(url_for('settings', item=device.device_name))

@app.route('/<item>/color/<color>')
def color(item, color):
    device = Device.query.filter_by(device_name=item)[0]
    device.color = color
    device.change_color = 1
    device.animation = 'none'
    db.session.commit()
    return redirect(url_for('settings', item=device.device_name))

@app.route('/<item>/animation/<animation>')
def animation(item, animation):
    device = Device.query.filter_by(device_name=item)[0]
    device.animation = animation
    db.session.commit()
    return redirect(url_for('settings', item=device.device_name))

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
    return redirect(url_for('settings',item=device.device_name))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(20), unique=True, nullable=False)
    on_off = db.Column(db.String(5), default='off', nullable=False)
    color = db.Column(db.String(20), default='white', nullable=False)
    brightness = db.Column(db.String(10),default='100',nullable=False)
    animation = db.Column(db.String(20), default=None)
    change_color = db.Column(db.String(10), default="0")

    def __repr__(self):
        return '<Device %r>' % self.device_name












if __name__ == "__main__":
    app.run(debug=True)
