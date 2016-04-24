import flask
from flask_socketio import join_room, send
import flask_socketio as sio
from init import app, db, socketio
import models


def check_request():
    token = flask.session['csrf_token']
    if flask.request.form['_csrf_token'] != token:
        app.logger.warn('invalid CSRF token')
        flask.abort(400)
    if flask.session.get('auth_user') != int(flask.request.form['creator_id']):
        app.logger.warn('requesting user %s not logged in (%s)',
                        flask.request.form['creator_id'],
                        flask.session.get('auth_user'))
        flask.abort(403)


@socketio.on('connect')
def on_connect():
    # get the connecting user's user ID
    # flask.session works in socket IO handlers :)
    uid = flask.session.get('auth_user', None)
    if uid is None:
        app.logger.warn('received socket connection from unauthed user')
        return

    app.logger.info('new client connected for user %d', uid)

    # add this connection to the user's 'room', so we can send to all
    # the user's open browser tabs
    join_room('user-{}'.format(uid))


@socketio.on('disconnect')
def on_disconnect():
    app.logger.info('client disconnected')
