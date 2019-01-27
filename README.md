# proto_qry

Protocol query from database

To run Flask devolopment server
* cd path_to_app_parent_folder
* call venv/Scripts/activate
* set FLASK_APP=proto_qry.py
* flask run --host=0.0.0.0




To run the docker image
$ docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=mysql1 -e MYSQL_USER=mysql1 \
    -e MYSQL_PASSWORD=<database-password> \
    mysql/mysql-server:8.0
    
    
    
docker network create my-custom-net

docker run --name=mysql1 --network=my-custom-net -d mysql/mysql-server
docker run --name=myapp1 --network=my-custom-net -d myapp

docker exec -it myapp1 mysql --host=mysql1 --user=myuser --password

This image exposes the standard MySQL port (3306), so container linking makes the MySQL instance available to other application containers. Start your application container like this in order to link it to the MySQL container:

$ docker run --name proto_qry --link mysql/mysql-server:8.0 -d proto_qry

$ docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=<password> -d mysql/mysql-server:8.0

Set up MYSQL:
* CREATE DATABASE md_length;
* Create new user to Database:
-- CREATE USER 'length'@'localhost' IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON md_length.* TO 'length'@'localhost';
-- FLUSH PRIVILEGES;
-- SHOW GRANTS FOR 'length'@'localhost';