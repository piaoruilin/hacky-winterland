DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS user_days;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT,
    img TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    img TEXT,
    external_link TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    img TEXT,
    external_link TEXT
);

CREATE TABLE user_days (
    user_id INTEGER,
    day_num INTEGER,
    movie_id INTEGER,
    song_id INTEGER,
    recipe_id INTEGER,
    img TEXT,
    PRIMARY KEY (user_id, day_num),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (song_id) REFERENCES songs(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
