-- Create database
CREATE DATABASE tasks_db;

-- Connect to the database
\c tasks_db;

-- Create table
CREATE TABLE tasks_db (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL
);
