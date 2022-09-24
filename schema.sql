CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    desprictions TEXT,
    instructions TEXT,
    author_id INTEGER NOT NULL REFERENCES users,
    created_on TIMESTAMP
);
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE ingredientsInRecipe (
    recipe_id INTEGER NOT NULL REFERENCES recipes,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients,
    amount INTEGER NOT NULL,
    unit TEXT NOT NULL
);
CREATE TABLE favourites (
    recipe_id INTEGER NOT NULL REFERENCES recipes,
    user_id INTEGER NOT NULL REFERENCES users
);
CREATE TABLE stars (
    recipe_id INTEGER NOT NULL REFERENCES recipes,
    star_rating INTEGER NOT NULL CHECK (
        star_rating >= 0
        AND star_rating <= 5
    )
);