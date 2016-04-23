import flask
import bcrypt
from init import app, db
import models


@app.route('/login')
def login():
    return flask.render_template('login.html')


@app.route('/username', methods=['POST'])
def handle_username():
    username = flask.request.form['login-username']
    password = flask.request.form['login-password']
    user = models.User.query.filter_by(username=username).first()
    if user is not None:
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        if pw_hash == user.pw_hash:
            flask.session['auth_user'] = user.id
            return flask.redirect(flask.request.form['url'], 303)
    return flask.render_template('login.html', state='bad')


@app.route('/create_user', methods=['POST'])
def create_user():
    username = flask.request.form['create-username']
    email = flask.request.form['email']
    password = flask.request.form['create-password']
    display = flask.request.form['display']
    if password != flask.request.form['create-confirm']:
        return flask.render_template('login.html', state='password-mismatch')
    if len(username) > 20:
        return flask.render_template('login.html', state='bad-username')
    existing = models.User.query.filter_by(username=username).first()
    if existing is not None:
        return flask.render_template('login.html', state='username-used')
    if set(' [~!@#$%^&*()_+{}":;\']+$').intersection(username):
        return flask.render_template('login.html', state='bad-username')
    if not username:
        return flask.render_template('login.html', state='bad-username')
    if not password:
        return flask.render_template('login.html', state='bad-password')

    user = models.User()
    user.username = username
    user.email = email
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))
    user.display = display
    db.session.add(user)
    db.session.commit()
    flask.session['auth_user'] = user.id
    return flask.redirect(flask.url_for('show_user', uid=user.id), 303)
