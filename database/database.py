import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432'
)

db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

cursor = db.cursor();

print("Connection database successfully.")

name_Database   = "chefencasa";
sqlDropeDatabase = "DROP DATABASE IF EXISTS " +name_Database + ";"
sqlCreateDatabase = "CREATE DATABASE "+name_Database+";"

cursor.execute(sqlDropeDatabase);
cursor.execute(sqlCreateDatabase);

print("The chefencasa database was created succesfully.")

db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database = name_Database
)
db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

cursor = db.cursor();

cursor.execute("CREATE TABLE IF NOT EXISTS category (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
cursor.execute("CREATE TABLE IF NOT EXISTS ingredient (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
cursor.execute("CREATE TABLE IF NOT EXISTS user_followers (id SERIAL PRIMARY KEY, id_user INT NOT NULL, id_chef_user INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_user) REFERENCES users(id), FOREIGN KEY (id_chef_user) REFERENCES users(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS recipes (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL, description TEXT, preparation_time_minutes INT, id_user INT NOT NULL, id_category INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_user) REFERENCES users(id), FOREIGN KEY (id_category) REFERENCES category(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS recipe_photos (id SERIAL PRIMARY KEY, url VARCHAR(255) NOT NULL, id_recipe INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_recipe) REFERENCES recipes(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS recipe_ingredients (id SERIAL PRIMARY KEY, id_ingredient INT NOT NULL, id_recipe INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_ingredient) REFERENCES ingredient(id), FOREIGN KEY (id_recipe) REFERENCES recipes(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS recipe_steps (id SERIAL PRIMARY KEY, description TEXT NOT NULL, id_recipe INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_recipe) REFERENCES recipes(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS user_favorite_recipes (id SERIAL PRIMARY KEY, id_user INT NOT NULL, id_recipe INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_user) REFERENCES users(id), FOREIGN KEY (id_recipe) REFERENCES recipes(id));")

print("The chefencasa database schema was created succesfully.")

cursor.execute("INSERT INTO ingredient (name) VALUES ('Tomate'), ('Cebolla'), ('Pimiento'), ('Ajo'), ('Aceite de oliva'),('Sal'), ('Pimienta'), ('Carne de res'), ('Pollo'), ('Pescado');")
cursor.execute("INSERT INTO category (name) VALUES ('Entrada'), ('Plato Principal'), ('Postre'), ('Aperitivo'), ('Ensalada'), ('Sopa'), ('Bebida'), ('Desayuno'), ('Cena'),('Snack');")
cursor.execute("INSERT INTO users (name, last_name, email, username, password) VALUES ('Juan', 'Perez', 'juan@example.com', 'juanperez', '1234'), ('Maria', 'Lopez', 'maria@example.com', 'marialopez', '1234'), ('Gonzalo', 'Ramirez', 'pedro@example.com', 'gonzaloramirez', '1234');")
cursor.execute("INSERT INTO user_followers (id_user, id_chef_user) VALUES ((SELECT id from users where username = 'juanperez'),(SELECT id from users where username = 'marialopez'))")
cursor.execute("INSERT INTO recipes (title, description, preparation_time_minutes, id_user, id_category) VALUES('Tarta de Manzana', 'Una deliciosa tarta de manzana casera.', 45, 1, 3), ('Pollo al Curry', 'Receta de pollo al curry con arroz basmati.', 60, 2, 2), ('Ensalada César', 'Ensalada fresca con aderezo César.', 20, 3, 5);")
cursor.execute("INSERT INTO recipe_photos (url, id_recipe) VALUES ('url_foto_tarta_manzana_1.jpg', 1), ('url_foto_tarta_manzana_2.jpg', 1), ('url_foto_tarta_manzana_3.jpg', 1);")
cursor.execute("INSERT INTO recipe_photos (url, id_recipe) VALUES ('url_foto_pollo_curry_1.jpg', 2), ('url_foto_pollo_curry_2.jpg', 2), ('url_foto_pollo_curry_3.jpg', 2);")
cursor.execute("INSERT INTO recipe_photos (url, id_recipe) VALUES ('url_foto_ensalada_cesar_1.jpg', 3), ('url_foto_ensalada_cesar_2.jpg', 3), ('url_foto_ensalada_cesar_3.jpg', 3);")
cursor.execute("INSERT INTO recipe_steps (description, id_recipe) VALUES ('Pelar y cortar las manzanas en rodajas finas.', 1), ('Forrar un molde con la masa para tarta.', 1), ('Colocar las manzanas sobre la masa.', 1), ('Hornear durante 35-40 minutos a 180°C.', 1);")
cursor.execute("INSERT INTO recipe_steps (description, id_recipe) VALUES ('Cortar el pollo en trozos pequeños.', 2), ('Freír el pollo en una sartén hasta que esté dorado.', 2), ('Agregar la mezcla de curry y cocinar durante 5 minutos.', 2), ('Servir el pollo al curry sobre arroz basmati.', 2);")
cursor.execute("INSERT INTO recipe_steps (description, id_recipe) VALUES ('Lavar y cortar la lechuga en trozos.', 3), ('Preparar la salsa César con mayonesa, ajo y limón.', 3), ('Mezclar la lechuga con la salsa y agregar crutones.', 3), ('Servir la ensalada César con parmesano rallado.', 3);")
cursor.execute("INSERT INTO recipe_ingredients (id_ingredient, id_recipe) VALUES (1, 1), (7, 1), (8, 1);")
cursor.execute("INSERT INTO recipe_ingredients (id_ingredient, id_recipe) VALUES (9, 2), (1, 2), (5, 2), (6, 2);")
cursor.execute("INSERT INTO recipe_ingredients (id_ingredient, id_recipe) VALUES (5, 3), (7, 3), (8, 3);")
cursor.execute("INSERT INTO user_favorite_recipes (id_user, id_recipe) VALUES (1, 1), (1, 3);")
cursor.execute("INSERT INTO user_favorite_recipes (id_user, id_recipe) VALUES (2, 2);")

print("Inserts ran succesfully.")

db.commit()
db.close()

print("The process finished successfully.")