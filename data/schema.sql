PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    user_id INTEGER NOT NULL,
    user_city VARCHAR(50) DEFAULT NULL,
    metric INTEGER CHECK (metric=0 OR metric=1) DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER,
    favorites_user_id INTEGER NOT NULL,
    user_favorite_city_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
    FOREIGN KEY (favorites_user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS current_weather (
    id INTEGER,
    current_weather_user_id INTEGER UNIQUE NOT NULL,
    wind_extended INTEGER CHECK (wind_extended=0 OR wind_extended=1) DEFAULT 0,
    pressure INTEGER CHECK (pressure=0 OR pressure=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (id)
    FOREIGN KEY (current_weather_user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS daily_weather (
    id INTEGER,
    daily_weather_user_id INTEGER UNIQUE NOT NULL,
    astro INTEGER CHECK (astro=0 OR astro=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (id)
    FOREIGN KEY (daily_weather_user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS hourly_weather (
    id INTEGER,
    hourly_weather_user_id INTEGER UNIQUE NOT NULL,
    wind_extended INTEGER CHECK (wind_extended=0 OR wind_extended=1) DEFAULT 0,
    pressure INTEGER CHECK (pressure=0 OR pressure=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (id)
    FOREIGN KEY (hourly_weather_user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS default_weather (
    id INTEGER,
    default_user_id INTEGER NOT NULL UNIQUE,
    current_weather INTEGER CHECK (current_weather=0 OR current_weather=1) DEFAULT 1,
    daily_weather INTEGER CHECK (daily_weather IN (1, 2, 3) ) DEFAULT 3,
    hourly_weather INTEGER CHECK (hourly_weather BETWEEN 1 AND 12) DEFAULT 6,
    PRIMARY KEY (id)
    FOREIGN KEY (default_user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS favorites_id_index ON favorites(id);
CREATE INDEX IF NOT EXISTS hourly_id_index ON hourly_weather(id);
CREATE INDEX IF NOT EXISTS daily_id_index ON daily_weather(id);
CREATE INDEX IF NOT EXISTS current_id_index ON current_weather(id);
CREATE INDEX IF NOT EXISTS users_user_id_index ON users (id);
CREATE INDEX IF NOT EXISTS default_user_id_index ON default_weather (id);