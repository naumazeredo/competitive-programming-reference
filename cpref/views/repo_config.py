from flask import jsonify
from flask_login import current_user
from cpref import app
from cpref.github import github_get_q


# TODO: remove
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


# TODO: remove
@app.route('/cpfiles')
def cpfiles():
    files = get_cpfiles()
    if files is None:
        return "No .cpref files :("
    return jsonify(files)


# TODO: remove (user-repos is the correct one)
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


@app.route('/config-repo/<repo_name>')
def config_repo(repo_name):
    return 'under construction'
