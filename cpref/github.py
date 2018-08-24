from flask_login import current_user
from cpref import oauth, db
from cpref.models import Token


def fetch_token():
    user = Token.query.filter_by(user_id=current_user.get_id()).first()
    if not user:
        return None
    return user.to_token()


def update_token(token):
    item = Token.query.filter_by(
        user_id=current_user.id
    ).first()

    if not item:
        item = Token(user_id=current_user.id)

    item.from_token(token)
    db.session.add(item)
    db.session.commit()
    return item


oauth.register(
    'github',
    api_base_url='https://api.github.com/',
    # request_token_params={'scope': 'user,repo'},
    request_token_url=None,
    # access_token_params={'scope': 'user,repo'},
    access_token_params=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    fetch_token=fetch_token,
    update_token=update_token,
    client_kwargs={'scope': 'read:user,write:repo_hook'}
)

github = oauth.github


# TODO: refactor
def github_get(resource, **kwargs):
    query = resource
    if bool(kwargs):
        query += '?' + \
                '&'.join("{!s}={!s}".format(k, v.replace(' ', '+'))
                         for (k, v)
                         in kwargs.items())
    print(query)
    resp = github.get(query)
    if resp.status_code != 200:
        print(resp)
        print(resp.json())
        return None
    return resp.json()


def github_get_q(resource, **kwargs):
    query = resource
    if bool(kwargs):
        query += '?q=' + \
                '+'.join("{!s}:{!s}".format(k, v.replace(' ', '+'))
                         for (k, v)
                         in kwargs.items())
    resp = github.get(query)
    if resp.status_code != 200:
        print(resp)
        print(resp.json())
        return None
    return resp.json()
