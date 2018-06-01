from flask_login import UserMixin
from cpref import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    avatar_url = db.Column(db.String(120))
    # email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Token(db.Model):
    __tablename__ = 'tokens'

    user_id = db.Column(db.Integer, primary_key=True)

    token_type = db.Column(db.String(20))
    access_token = db.Column(db.String(48), nullable=False)
    refresh_token = db.Column(db.String(48))
    expires_at = db.Column(db.Integer, default=0)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at
        )

    def from_token(self, token):
        self.access_token = token.get('access_token')
        self.token_type = token.get('token_type', 'bearer')
        self.refresh_token = token.get('refresh_token')
        self.expires_at = token.get('expires_at', 0)


class Repo(db.Model):
    __tablename__ = 'repos'

    repo_id = db.Column(db.Integer, primary_key=True)
    hook_id = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime)


# TODO: Create Webhooks class
