from flask_login import current_user
from cpref import db
from cpref.github import github, github_get, github_get_q
from cpref.models import Repo


params = {
    'name': 'web',
    'active': True,
    'events': ['push'],
    'config': {
        'url': 'http://92709ba1.ngrok.io/webhook',
        'content_type': 'json',
        'insecure_ssl': '0',
    }
}


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


def get_hook_list(repo_name):
    resp = github_get("/repos/{!s}/{!s}/hooks".format(current_user.login,
                                                      repo_name))
    return resp


# TODO: change to get_webhook_status (None: no webhook, "ok", "misconfigured")
def has_webhook(repo_name):
    repo = Repo.query.filter_by(
        user_login=current_user.login,
        repo_name=repo_name
    ).first()

    # XXX: Check if the repo is on database and if it's configured correctly on server

    if repo:
        return True

    hook_list = get_hook_list(repo_name)

    # TODO: tell between installed correctly and misconfigured
    # FIXME: it's only valid if events == ['push'] (what to do?)
    for hook in hook_list:
        if params.items() <= hook.items():
            return True
    return False


def create_webhook(repo_name):
    # XXX: if on database and on server        : (do nothing) already installed
    # XXX: if on database and not on server    : (update) misconfigured 1
    # XXX: if not on database and on server    : (update) misconfigured 2
    # XXX: if not on database and not on server: (create) not installed

    if has_webhook(repo_name):
        return {'status': 'error', 'data': 'Webhook already installed'}

    # TODO: refactor github.post (with github_get/github_get_q)
    query = "/repos/{!s}/{!s}/hooks".format(current_user.login, repo_name)
    resp = github.post(query, json=params)

    if resp.status_code != 201:
        return {'status': 'error', 'data': resp.json()}

    resp = resp.json()

    repo = Repo(
        hook_id=resp['id'],
        repo_name=repo_name,
        user_login=current_user.login
    )

    db.session.add(repo)
    db.session.commit()

    return {'status': 'ok', 'data': resp, 'repo': repo}


# TODO: create update-repo
def update_repo(repo_name):
    pass


# TODO: create
def is_repo_uptodate(repo):
    if not repo:
        # XXX: log error: calling function for repo not in database
        return False

    return False
