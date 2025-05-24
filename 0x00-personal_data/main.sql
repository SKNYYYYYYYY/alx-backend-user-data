-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO 'root'@'localhost';

USE my_db;

CREATE TABLE pii_users (
    email VARCHAR(256)
);
INSERT INTO pii_users(email) VALUES ("bob@dylan.com");
INSERT INTO pii_users(email) VALUES ("bib@dylan.com");