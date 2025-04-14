-- SQL Scripts for Table Generation and Initial Data

-- Create database hbnb_evo_2_db
CREATE DATABASE IF NOT EXISTS hbnb_evo_2_db;
USE hbnb_evo_2_db;

DROP TABLE IF EXISTS users;
-- User Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` VARCHAR(60) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS places;
-- Place Table
CREATE TABLE IF NOT EXISTS `places` (
    `id` VARCHAR(60),
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `price` FLOAT NOT NULL,
    `latitude` FLOAT NOT NULL UNIQUE,
    `longitude` FLOAT NOT NULL UNIQUE,
    `owner_id` VARCHAR(60) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `ibfk_places` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS reviews;
-- Review Table
CREATE TABLE IF NOT EXISTS `reviews` (
    `id` VARCHAR(60) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `text` TEXT NOT NULL,
    `rating` INT NOT NULL,
    `user_id` VARCHAR(60),
    `place_id` VARCHAR(60) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `ibfk_reviews_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
    CONSTRAINT `ibfk_reviews_2` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `amenities`;
-- Amenity Table
CREATE TABLE IF NOT EXISTS `amenities` (
    `id` VARCHAR(60),
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `place_amenity`;
-- Place Amenity Table
CREATE TABLE IF NOT EXISTS `place_amenity` (
    `place_id` VARCHAR(60) NOT NULL,
    `amenity_id` VARCHAR(60) NOT NULL,
    PRIMARY KEY (`place_id`, `amenity_id`),
    CONSTRAINT `ibfk_place_amenity_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
    CONSTRAINT `ibfk_place_amenity_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

-- Administrator User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', 'admin1234', true);

-- Amenities
INSERT INTO amenities (id, name)
VALUES ('31940963-ccee-45d6-8188-78d00eb1b958', 'WiFi');
INSERT INTO amenities (id, name)
VALUES ('2af6e1df-7cef-4e7c-b232-e411a47bdaa0', 'Swimming Pool');
INSERT INTO amenities (id, name)
VALUES ('554fe2de-2694-4475-8456-81508a207147', 'Air Conditioning');
