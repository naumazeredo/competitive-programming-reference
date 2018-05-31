from cpref.github import github


# TODO: refactor!


def github_get(resource, **kwargs):
    query = resource
    if len(kwargs) != 0:
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
    if len(kwargs) != 0:
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
