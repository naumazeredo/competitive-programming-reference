from cpref import app, db


if __name__ == '__main__':
    if app.config['ENV'] == 'development':
        db.create_all()
        app.run(use_reloader=True)
    else:
        app.run('0.0.0.0', port=4242)
