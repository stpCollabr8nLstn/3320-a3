import flask
import flask_socketio as sio
import re
import urllib
from init import app, db, socketio
import models
import io
import base64
import os


@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


@app.before_request
def setup_user():
    if 'auth_user' in flask.session:
        user = models.User.query.get(flask.session['auth_user'])
        if user is None:
            del flask.session['auth_user']
        flask.g.user = user


@app.route('/')
def index():
    rooms = models.Room.query.order_by(models.Room.topic).limit(20).all()
    return flask.render_template('index.html', csrf_token=flask.session['csrf_token'], rooms=rooms)


@app.route('/user/<int:uid>')
def show_user(uid):
    user = models.User.query.get_or_404(uid)
    return flask.render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    del flask.session['auth_user']
    return flask.redirect(flask.url_for('login'))


@app.route('/edit_user/<int:uid>')
def edit_user(uid):
    user = models.User.query.get_or_404(uid)
    return flask.render_template('edit_user.html', user=user)


@app.route('/create_room', methods=['POST'])
def create_room():
    topic = flask.request.form['topic']
    room = models.Room()
    room.topic = topic
    db.session.add(room)
    db.session.commit()
    r_id = room.id
    return flask.redirect(flask.url_for('room_view', r_id=r_id), code=303)


@app.route('/room/<int:r_id>')
def room_view(r_id):
    room = models.Room.query.filter_by(id=r_id).first()
    return flask.render_template('room.html', room=room)


@app.errorhandler(404)
def not_found(err):
    return flask.render_template('404.html', path=flask.request.path), 404