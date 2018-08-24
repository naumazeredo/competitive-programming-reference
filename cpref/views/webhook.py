from flask import request
from flask_login import login_required
from cpref import app
from cpref.models import Repo


# TODO: call update_repo
@app.route('/webhook', methods=['POST'])
def webhook_callback():
    print(request.get_json())
    return ""
