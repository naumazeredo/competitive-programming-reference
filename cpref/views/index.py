from flask import render_template
from flask_login import current_user
from cpref import app


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Home',
        current_user=current_user
    )
