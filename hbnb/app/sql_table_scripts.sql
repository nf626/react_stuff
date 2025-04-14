-- Create User Table in hbnb_evo_2_db Database
CREATE DATABASE IF NOT EXISTS hbnb_evo_2_db;
USE hbnb_evo_2_db;
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36), 
    PRIMARY KEY (uuid),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    `password` VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36), 
    PRIMARY KEY (uuid),
    title VARCHAR(255),
    `description` TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36), 
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) 
    PRIMARY KEY (uuid.uuid4()),
    `text` TEXT,
    rating INT,
    user_id CHAR(36), 
    FOREIGN KEY (user_id) REFERENCES users(id)
    place_id: CHAR(36), 
    FOREIGN KEY (place_id) REFERENCES places(id)
    -- Add a unique constraint on the combination of user_id and place_id to ensure that a user can only leave one review per place.
);

CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36),
    PRIMARY KEY (uuid),
    `name` VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES places(id)
    amenity_id CHAR(36), 
    FOREIGN KEY (amenity_id_id) REFERENCES amenity(id),
    PRIMARY KEY (place_id, amenity_id)
    -- Add a composite primary key for place_id and amenity_id.
);

INSERT INTO users (id, first_name, last_name, email, `password`, is_admin) VALUES("36c9050e-ddd3-4c3b-9731-9f487208bbc1", "Admin", "HbnB", "admin123", "true");

INSERT INTO amenities (`name`) VALUES ("WiFi"), ("Swimming Pool"), ("Air conditioning")
