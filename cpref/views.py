from flask import url_for, flash, redirect, jsonify, request
from flask_login import current_user, login_user, logout_user
from cpref import app, db, login_manager
from cpref.models import User
from cpref.github import github, update_token
from cpref.utils import github_get, github_get_q


@app.route('/')
def index():
    # if 'github_token' in session:
    if current_user.is_authenticated:
        me = github_get('/user')
        if me is None:
            return redirect(url_for('logout'))
        return jsonify(me)

    # flash('Redirecting to login!')
    # return redirect(url_for('login'))
    return 'Not an user! <a href="/login">Login</a>'


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    # session.pop('github_token', None)
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    # session['github_token'] = token

    github_user = github_get('/user')

    if not github_user:
        flash("Could not find user!")
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


@app.route('/repos')
def repos():
    repos_json = github_get('/user/repos', affiliation='owner')
    repos_list = list(map(lambda x: x['full_name'], repos_json))
    return jsonify(repos_list)


def get_cpfiles():
    files_json = github_get_q(
        '/search/code',
        filename='.cpref',
        path='/',
        user=current_user.login
    )

    if files_json is None:
        return None

    return files_json['items']


@app.route('/cpfiles')
def cpfiles():
    files = get_cpfiles()
    if files is None:
        return "No .cpref files :("
    return jsonify(files)


@app.route('/valid-repos')
def valid_repos():
    files = get_cpfiles()

    if not files:
        return "No valid repository. Create a .cpref file"

    repos_dict = {}
    for cpfile in files:
        repo_id = cpfile['repository']['id']
        repo_name = cpfile['repository']['name']
        repos_dict[repo_id] = repo_name

    return jsonify(repos_dict)


@app.route('/webhook', methods=['POST'])
def webhook_callback():
    print(request.get_json())
    return ""


def create_webhook(repo_name):
    params = {
        'name': 'web',
        'active': True,
        'events': ['push'],
        'config': {
            'url': 'http://92709ba1.ngrok.io/webhook',
            'content_type': 'json'
        }
    }

    query = "/repos/{!s}/{!s}/hooks".format(current_user.login, repo_name)
    resp = github.post(query, json=params)

    if resp.status_code != 201:
        print(resp)
        print(resp.json())
        return None

    return resp.json()


@app.route('/create-hook/<repo_name>')
def create_hook(repo_name):
    resp = create_webhook(repo_name)
    if resp is None:
        return 'Could not create webhook!'
    return jsonify(resp)


@app.route('/list-hooks/<repo_name>')
def list_hooks(repo_name):
    resp = github_get("/repos/{!s}/{!s}/hooks".format(current_user.login,
                                                      repo_name))
    if resp is None:
        return 'Error!'
    return jsonify(resp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
