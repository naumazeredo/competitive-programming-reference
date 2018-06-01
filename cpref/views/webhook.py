from flask import request, jsonify
from flask_login import current_user
from cpref import app
from cpref.github import github, github_get, webhook_params


# TODO: call update_repo
@app.route('/webhook', methods=['POST'])
def webhook_callback():
    print(request.get_json())
    return ""


def create_webhook(repo_name):
    query = "/repos/{!s}/{!s}/hooks".format(current_user.login, repo_name)
    resp = github.post(query, json=webhook_params)

    if resp.status_code != 201:
        print(resp)
        print(resp.json())
        return None

    return resp.json()


# TODO: remove
@app.route('/create-hook/<repo_name>')
def create_hook(repo_name):
    resp = create_webhook(repo_name)
    if resp is None:
        return 'Could not create webhook!'
    return jsonify(resp)


# TODO: remove
@app.route('/list-hooks/<repo_name>')
def list_hooks(repo_name):
    resp = github_get("/repos/{!s}/{!s}/hooks".format(current_user.login,
                                                      repo_name))
    if resp is None:
        return 'Error!'
    return jsonify(resp)
