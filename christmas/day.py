from flask import Blueprint, render_template, request, g
from werkzeug.utils import redirect
from christmas.auth import login_required

from christmas.db import get_db

bp = Blueprint("day", __name__)

MOVIES_NUM = 13
RECIPES_NUM = 12

@bp.route("/day/<day_num>", methods=["GET", "POST"])
def day(day_num):
    FALLBACK_INFO = {
        "name": "Fallback Name",
        "title": "Fallback Title",
        "artist": "Fallback Artist",
        "link": "/static/song-mp3/1-Happy_Xmas.mp3",
        "external_link": "https://duckduckgo.com/?t=ffab",
        "img": "/static/song-img/1-Happy_Xmas_John_Lennon.jpg",
        "description": "Fallback description"
    }

    db = get_db()

    if g.user is None:
        is_logged_in = False
    else:
        is_logged_in = True

    if is_logged_in:
        user_info = g.user
        user_num = g.user["id"]
    else:
        user_num = 1
        user_info = db.execute(
            "SELECT * FROM user WHERE id = 1"
        ).fetchone()

    day_info = db.execute(
        "SELECT * FROM user_days WHERE user_id = ? AND day_num = ?", (
            user_num, day_num)
    ).fetchone()

    if day_info is None:
        day_info = {
            "day_num": 1,
            "img": "/static/santa/bell.png",
            "movie_id": 1,
            "song_id": 1,
            "recipe_id": 1
        }

    movie_info = db.execute(
        "SELECT * FROM movies WHERE id = ?", (day_info["movie_id"], )
    ).fetchone()

    if movie_info is None:
        movie_info = FALLBACK_INFO

    recipe_info = db.execute(
        "SELECT * FROM recipes WHERE id = ?", (day_info["recipe_id"], )
    ).fetchone()

    if recipe_info is None:
        recipe_info = FALLBACK_INFO

    song_info = db.execute(
        "SELECT * FROM songs WHERE id = ?", (day_info["song_id"], )
    ).fetchone()

    if song_info is None:
        song_info = FALLBACK_INFO

    day_links = ["/day/"+str(day_num) for day_num in range(1, 13)]

    all_movies = db.execute(
        "SELECT id, title FROM movies"
    ).fetchall()

    all_recipes = db.execute(
        "SELECT id, name FROM recipes"
    ).fetchall()

    all_recipes = db.execute(
        "SELECT id, name FROM recipes"
    ).fetchall()

    return render_template("day.html",
        recipes_num=RECIPES_NUM,
        all_recipes=all_recipes,
        movies_num=MOVIES_NUM,
        all_movies=all_movies,
        day_links=day_links,
        logged_in=is_logged_in,
        day_info=day_info,
        movie_info=movie_info,
        recipe_info=recipe_info,
        song_info=song_info,
        notes=user_info["notes"]
    )

@login_required
@bp.route("/update_<item>", methods=["POST"])
def update_movies(item):

    if g.user is None:
        return redirect("/auth/login")

    user_id = g.user["id"]
    day_num = request.form.get("day_num")
    db = get_db()

    if item == "movie":
        movie = request.form.get("movie")
        db.execute(
            "UPDATE user_days SET movie_id=? WHERE user_id=? AND day_num=?",
            (movie, user_id, day_num)
        )
        db.commit()
    elif item == "recipe":
        recipe = request.form.get("recipe")
        db.execute(
            "UPDATE user_days SET recipe_id=? WHERE user_id=? AND day_num=?",
            (recipe, user_id, day_num)
        )
        db.commit()

    return redirect("/day/" + day_num)


@login_required
@bp.route("/update_notes", methods=["POST"])
def update_notes():

    if g.user is None:
        return redirect("/auth/login")

    user_id = g.user["id"]
    day_num = request.form.get("day_num")
    notes = request.form.get("notes")
    db = get_db()

    db.execute(
        "UPDATE user SET notes=? WHERE id=?", (notes, user_id)
    )
    db.commit()

    return redirect("/day/" + day_num)
