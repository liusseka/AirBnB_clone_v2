-- prepares a server for this project
-- creates db, test user, and grants permissions
CREATE DATABASE hbnb_test_db;
CREATE USER 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db . * TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance schema . * TO 'hbnb_test'@'localhost';
