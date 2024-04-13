CREATE TABLE location (
    ip VARCHAR(255) PRIMARY KEY,
    lat REAL,
    long REAL,
    country_long VARCHAR(255),
    country_short VARCHAR(2),
    region VARCHAR(255),
    city VARCHAR(255),
    zip_code VARCHAR(255),
    tzone VARCHAR(255)
);

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(255),
    port INT,
    dt INT
);
