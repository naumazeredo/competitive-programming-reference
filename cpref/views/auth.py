from flask import url_for, redirect
from flask_login import login_user, logout_user
from cpref import app, db, login_manager
from cpref.models import User
from cpref.github import github, update_token, github_get


# TODO: create page
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    # session['github_token'] = token

    github_user = github_get('/user')

    if not github_user:
        # flash("Could not find user!")
        redirect(url_for('login'))

    user = User.query.filter_by(id=github_user['id']).first()

    if not user:
        user = User(id=github_user['id'])

    user.login = github_user['login']
    user.avatar_url = github_user['avatar_url']
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    update_token(token)

    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
