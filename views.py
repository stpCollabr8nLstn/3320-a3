import base64
import flask
import models
import os
from sqlalchemy.orm import joinedload
from init import app, db
from sqlalchemy import or_
from sqlalchemy import desc


@app.route('/user/<int:uid>')
def show_user(uid):
    user = models.User.query.get_or_404(uid)
    return flask.render_template('user.html')