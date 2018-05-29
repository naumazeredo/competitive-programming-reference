from cpref import app, github, db
from cpref.models import User
from flask import Flask, request, url_for, flash, redirect, session, jsonify


@app.route('/')
def index():
    if 'github_token' in session:
        print(session)
        me = github.get('user').json()
        return jsonify(me)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

    '''
    return github.authorize(callback=url_for('authorized',
        #next=request.args.get('next') or request.referrer or None,
        _external=True))
        '''

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    session['github_token'] = token
    me = github.get('user').json()
    return jsonify(me)

    """
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
            return 'Access denied: reason=%s error=%s resp=%s' % (
                request.args['error'],
                request.args['error_description'],
                resp
            )

    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    return jsonify(me.data)
    """

    """
    if response == 'access_denied':
        return 'Access denied'

    flash('You have been logged in to GitHub successfully')
    session['access_token'] = access_token

    return redirect(url_for('index'))
    """

    """
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User(github_access_token=oauth_token)
        db.session.add(user)

    user.github_access_token = oauth_token
    db.session.commit()
    return redirect(next_url)
    """


'''
@app.route('/repo')
def repo():
    repo_dict = github.get('/user/repos')
    return str(repo_dict)
'''
