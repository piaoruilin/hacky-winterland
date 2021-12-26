import os
from flask import Flask, g
from flask.templating import render_template
from christmas.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = 'dev'
    app.config["DATABASE"] = os.path.join(app.instance_path, 'christmas.sqlite')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import internal
    app.register_blueprint(internal.bp)
    
    from . import day
    app.register_blueprint(day.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        db = get_db()
        if g.user is None:
            is_logged_in = False
        else:
            is_logged_in = True

        if is_logged_in:
            user_num = g.user["id"]
        else:
            user_num = 1

        days = []
        day_links = ["/day/"+str(day_num) for day_num in range(1, 13)]
        for day_num in range(1, 13):
            day_info = db.execute(
                "SELECT * FROM user_days WHERE user_id = ? AND day_num = ?", (user_num, day_num)
            ).fetchone()
            days.append(day_info)
        
        return render_template('index.html', 
            logged_in=is_logged_in,
            days=days, 
            day_links=day_links
        )

    return app