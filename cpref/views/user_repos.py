from flask import jsonify
from cpref import app
from cpref.github import github_get


# TODO: create page
@app.route('/user-repos')
def user_repos():
    repos_json = github_get('/user/repos', affiliation='owner')
    repos_list = list(map(lambda x: x['full_name'], repos_json))
    return jsonify(repos_list)
