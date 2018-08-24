from flask import render_template, jsonify
from flask_login import current_user, login_required
from cpref import app
from cpref.repo_utils import has_webhook, create_webhook, get_cpfiles




@app.route('/user-repos')
@login_required
def user_repos():
    files = get_cpfiles()

    repos = []
    for cpfile in files:
        repo_name = cpfile['repository']['name']
        repos.append({'name': repo_name, 'webhook': has_webhook(repo_name)})

    return render_template(
        'user-repos.html',
        current_user=current_user,
        repos=repos
    )


# TODO: create
@app.route('/user-repo/<repo_name>')
@login_required
def user_repo(repo_name):
    return 'under construction'


@app.route('/user-repo/<repo_name>/add')
@login_required
def user_repo_add(repo_name):
    resp = create_webhook(repo_name)
    # TODO: correctly show errors
    if resp['status'] == 'error':
        return jsonify(resp['data'])

    # TODO: update_repo

    # TODO: redirect to /user-repos with flash
    return jsonify(resp['data'])


# TODO: create
@app.route('/user-repo/<repo_name>/delete')
@login_required
def user_repo_delete(repo_name):
    return 'under construction'
