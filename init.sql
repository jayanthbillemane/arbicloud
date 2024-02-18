-- Create database
CREATE DATABASE tasks;

-- Connect to the database
\c tasks;

-- Create table
CREATE TABLE list_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL
);
