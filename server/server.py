from servicio_pb2_grpc import ChefEnCasaServicer, add_ChefEnCasaServicer_to_server
from servicio_pb2 import ResponseUser, ResponseIngredients, Ingredient, Category , ResponseCategorys, ResponseRecipes, Reciepe,Photo, User, Response, ResponseRecipe, Stept, ResponseComments, Comment, ResponseUsers, ResponseNovedades, Novedad
from confluent_kafka import Producer,Consumer,KafkaError
import time
import grpc
import datetime
import json
from concurrent import futures

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db = psycopg2.connect(
    user="postgres",
    password="1234",
    host="localhost",
    port='5432',
    database = "chefencasa"
)

cursor = db.cursor()

# Configuración del productor
producer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'client.id': 'python-producer'
}

#Crear un productor Kafka
producer = Producer(producer_config)

class ServiceChefEnCasa(ChefEnCasaServicer):
    def CreateRecipe(self, request, context):
        print("CreateRecipe")
        print(request)
        try:
            query = "INSERT INTO recipes (title, description, preparation_time_minutes, id_user, id_category) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}') RETURNING id;".format(request.title,request.description,request.prepatarionTimeMinutes,request.idUser,request.category.id)
            cursor.execute(query)
            result = cursor.fetchone()
            idRecipe = result[0]
            print(idRecipe)
            db.commit()
            for photo in request.photos:
                query = "INSERT INTO recipe_photos (url,id_recipe) VALUES ('{0}','{1}') ;".format(photo.url,idRecipe)
                cursor.execute(query)
            for stept in request.stepts:
                print(stept)
                query = "INSERT INTO recipe_steps (description,id_recipe) VALUES  ('{0}','{1}');".format(stept.description,idRecipe)
                cursor.execute(query)
            for ingredient in request.ingredients:
                query = "INSERT INTO recipe_ingredients (id_ingredient,id_recipe) VALUES('{0}','{1}')".format(ingredient.id,idRecipe)
                cursor.execute(query)
            db.commit()
            

            #Agregar al topic Novedades
            topic_name = 'Novedades'

            #Datos receta
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idUser)
            cursor.execute(query)
            result = cursor.fetchone()
            
            nombre_usuario = result[3]
            titulo_receta = "'{0}'".format(request.title)
            url_foto = "'{0}'".format(request.photos[0].url)            

            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            mensaje_receta_data = {
                'Usuario': nombre_usuario,
                'title': request.title,
                'URL Foto': request.photos[0].url
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_receta_json = json.dumps(mensaje_receta_data)

            # Enviar el mensaje al topic "Novedades" con los encabezados
            producer.produce(topic=topic_name, value=mensaje_receta_json, headers=headers)

            # Espera a que todos los mensajes se envíen
            producer.flush()                         

            return Response(message = '{0}'.format(idRecipe))
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "-1")
    def AddReciepeToFavorites(self, request, context):
        print("like")
        print("-----------------AddRecipeToFavorites---------------")
        print(request)
        query = "INSERT INTO user_favorite_recipes (id_user, id_recipe) VALUES ('{0}', '{1}') RETURNING id;".format(request.idUser, request.idReciepe)
        print(0.5)
        try:
            print(1)
            cursor.execute(query)
            print(2)
            result = cursor.fetchone()
            print(3)
            idUser = result[0]
            print(4)
            print(idUser)
            print(5)
            db.commit()
            print(6)
            
            #Mesanje para el topic "PopularidadReceta"
            puntaje = 1
            mensaje_popularidad = {
                'IdReceta': request.idReciepe,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadReceta" con los encabezados
            producer.produce(topic='PopularidadReceta', value=mensaje_popularidad_json, headers=headers)

            producer.flush() 
            print("Guardado en el topic de PopularidadReceta")  


            # Envía un mensaje al topic PopularidadUsuario
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idUser)
            cursor.execute(query)
            result = cursor.fetchone()
            
            nombre_usuario = result[3]
            
            puntaje = 1
            mensaje_popularidad = {
                'nombreUsuario': nombre_usuario,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadUsuario" con los encabezados
            producer.produce(topic='PopularidadUsuario', value=mensaje_popularidad_json, headers=headers)

            producer.flush()   

            return Response(message = '{0}'.format(1))
        except BaseException as error:
            print("me mori")
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "-1")
    def RemoveReciepeToFavorites(self, request, context):
        print("dislike")
        print(request)
        query = "DELETE FROM user_favorite_recipes WHERE id_user = {0} AND id_recipe = {1}".format(request.idUser, request.idReciepe)
        try:
            cursor.execute(query)
            db.commit()
            #Mesanje para el topic "PopularidadReceta"
            puntaje = -1
            mensaje_popularidad = {
                'IdReceta': request.idReciepe,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadReceta" con los encabezados
            producer.produce(topic='PopularidadReceta', value=mensaje_popularidad_json, headers=headers)

            producer.flush()  

            # Envía un mensaje al topic PopularidadUsuario
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idUser)
            cursor.execute(query)
            result = cursor.fetchone()
            
            nombre_usuario = result[3]
            
            puntaje = -1
            mensaje_popularidad = {
                'nombreUsuario': nombre_usuario,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadUsuario" con los encabezados
            producer.produce(topic='PopularidadUsuario', value=mensaje_popularidad_json, headers=headers)

            producer.flush()   

            return Response(message = 1)
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "-1")
    def GetAllFavoritesReciepes(self, request, context):
        print("--------------GetAllFavoritesReciepes-----------------")
        print("request")
        print(request)

        try:
            query_recipes = """
<<<<<<< HEAD
            SELECT * FROM recipes as r where isDraft = 0 and r.id in (SELECT id_recipe FROM user_favorite_recipes as ufr WHERE ufr.id_user = {0})
=======
            SELECT id, title, description, preparation_time_minutes, id_user, id_category,  created_at, updated_at FROM recipes as r where r.id in (SELECT id_recipe FROM user_favorite_recipes as ufr WHERE ufr.id_user = {0})
>>>>>>> 687c95877ed8a5141eacaa7e5a4f5cb1665c9d0b
        """.format(request.id)
            
            cursor.execute(query_recipes)

            column_names = [desc[0] for desc in cursor.description]
            print(column_names)
            allRecipes = []
            for row in cursor.fetchall():
                print("row")
                print(row)

                query_photos = """
                    SELECT * FROM recipe_photos as rp WHERE rp.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_photos)
                photos = []

                

                for row_photo in cursor.fetchall():
                    photo = Photo(id = row_photo[0], url = row_photo[1])
                    photos.append(photo)


                query_ingredients = """
                    SELECT i.id, i.name FROM recipe_ingredients as ri INNER JOIN ingredient as i ON ri.id_ingredient = i.id WHERE ri.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_ingredients)
                ingredients = []
                for row_ingredient in cursor.fetchall():
                    ingredient = Ingredient(id = row_ingredient[0], name = row_ingredient[1])
                    ingredients.append(ingredient)


                print("ingredients")
                print(ingredients)

                query_category = """
                    SELECT c.id, c.name FROM category as c WHERE c.id = {0}
                    """.format(row[5])
                cursor.execute(query_category)
                result_category = cursor.fetchone()
                category = Category(id = result_category[0], name = result_category[1])

                print(2)
                print("row[0]")
                print(row)

                query_user = """
                    SELECT u.id, u.name, u.last_name, u.username FROM users as u WHERE u.id = {0}
                    """.format(row[4])
                cursor.execute(query_user)
                result_user = cursor.fetchone()
                print("result_user")
                print(result_user)
                user = User(id = result_user[0], name = result_user[1], userName = result_user[2])



                print("ingredients")
                print(ingredients)

                print("user")
                print(user)

                print("category")
                print(category)



                recipe = Reciepe(idReciepe = row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category, prepatarionTimeMinutes=row[3], user=user)
                allRecipes.append(recipe)
            return ResponseRecipes(recipes = allRecipes)

        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")

    def GetRecipiesByFilters(self, request, context):
        print("--------------GetRecipiesByFilters-----------------")
        
        print("prepTime")
        print(request.prepatarionTimeMinutesMax)
        print("title")
        print(request.title)
        print("category")
        print(request.category.id)

        allRecipes = []

        try:
            # preparation_time_minutes lower than
            # title contains

            # only add category if is not -1
            # only add title if is not "."
            # only add preparation_time_minutes if is not 0

            category_where = "r.id_category = {0}".format(request.category.id) if (request.category.id != -1) else "r.id_category > 0"
            title_where = "lower(title) like '%{0}%'".format(request.title.lower()) if request.title != "." else "lower(title) like '%%'"
            prep_time_where = "r.preparation_time_minutes <= {0}".format(request.prepatarionTimeMinutesMax) if request.prepatarionTimeMinutesMax != 0 else "r.preparation_time_minutes > 0"

            query_recipes = """
                SELECT * FROM recipes as r where {0} and {1} and {2} and r.isDraft = 0
            """.format(category_where, title_where, prep_time_where)
            
            # query_recipes = """
            #     SELECT * FROM recipes as r where r.id_category = {0} and title like '%{1}%' and r.preparation_time_minutes <= {2} and r.isDraft = 0
            # """.format(request.category.id, "" if request.title.lower() == "." else request.title.lower(), request.prepatarionTimeMinutesMax)

            # print("catId")
            # print(request.category.id)

            # if (request.category.id > 1):
            #     query_recipes = """
            #         SELECT * FROM recipes as r where lower(title) like '%{0}%' and r.preparation_time_minutes <= {1} and r.isDraft = 0
            #     """.format(request.title.lower(), request.prepatarionTimeMinutesMax)
            #     if (request.title == "." or request.title == "" or request.title == " " or request.title == None):
            #         query_recipes = """
            #             SELECT * FROM recipes as r where r.preparation_time_minutes <= {0} and r.isDraft = 0
            #         """.format(request.prepatarionTimeMinutesMax)
            #         if (request.category.id != -1):
            #             query_recipes = """
            #                 SELECT * FROM recipes as r where r.preparation_time_minutes <= {0} and r.isDraft = 0
            #             """.format(request.prepatarionTimeMinutesMax) 
            # if ((request.title == "." or request.title == "" or request.title == " " or request.title == None) and request.category.id != -1):
            #     query_recipes = """
            #         SELECT * FROM recipes as r where r.id_category = {0} and r.isDraft = 0
            #     """.format(request.category.id)

            print(query_recipes)
            

            cursor.execute(query_recipes)

            column_names = [desc[0] for desc in cursor.description]
            print(column_names)
           
            for row in cursor.fetchall():
                print(row)

                query_photos = """
                    SELECT * FROM recipe_photos as rp WHERE rp.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_photos)
                photos = []

                

                for row_photo in cursor.fetchall():
                    photo = Photo(id = row_photo[0], url = row_photo[1])
                    photos.append(photo)


                query_ingredients = """
                    SELECT i.id, i.name FROM recipe_ingredients as ri INNER JOIN ingredient as i ON ri.id_ingredient = i.id WHERE ri.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_ingredients)
                ingredients = []
                for row_ingredient in cursor.fetchall():
                    ingredient = Ingredient(id = row_ingredient[0], name = row_ingredient[1])
                    ingredients.append(ingredient)


                print("ingredients")
                print(ingredients)

                query_category = """
                    SELECT c.id, c.name FROM category as c WHERE c.id = {0}
                    """.format(row[5])
                cursor.execute(query_category)
                result_category = cursor.fetchone()
                category = Category(id = result_category[0], name = result_category[1])

                print(2)

                query_user = """
                    SELECT u.id, u.name, u.last_name, u.username FROM users as u WHERE u.id = {0}
                    """.format(row[4])
                cursor.execute(query_user)
                result_user = cursor.fetchone()
                user_recipe = User(id = result_user[0], name = result_user[1], userName = result_user[2])



                print("ingredients")
                print(ingredients)

                print("user")
                print(user_recipe)

                print("category")
                print(category)



                recipe = Reciepe(idReciepe = row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category, prepatarionTimeMinutes=row[3], user=user_recipe)
                allRecipes.append(recipe)
            return ResponseRecipes(recipes = allRecipes)

        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseRecipes(recipes = allRecipes)

            

    
    def GetAllCategorys(self, request, context):
        allCategorys = []
        try:
            query = "SELECT c.id , c.name FROM category as c"
            cursor.execute(query)
            for row in cursor.fetchall():
                category = Category(id = row[0] , name = row[1])
                allCategorys.append(category)
            return ResponseCategorys(categorys = allCategorys)

        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseCategorys(categorys = allCategorys)

    def GetAllIngredients(self, request, context):
        allIngredients = []
        try:
            query = "SELECT i.id , i.name FROM ingredient as i"
            cursor.execute(query)
            for row in cursor.fetchall():
                ingredient = Ingredient(id = row[0] , name = row[1])
                allIngredients.append(ingredient)
            return ResponseIngredients(ingredients = allIngredients)

        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseIngredients(ingredients = allIngredients)
    def GetAllRecipes(self, request, context):
        allRecipes = []
        print("---------------GetAllRecipes---------------")
        try:

            # inner join for recipe_photos and recipe_ingredients

            query_recipes = """
            SELECT * FROM recipes as r
            """
            cursor.execute(query_recipes)

            column_names = [desc[0] for desc in cursor.description]
            print(column_names)
           
            for row in cursor.fetchall():
                print(row)

                query_photos = """
                    SELECT * FROM recipe_photos as rp WHERE rp.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_photos)
                photos = []

                

                for row_photo in cursor.fetchall():
                    photo = Photo(id = row_photo[0], url = row_photo[1])
                    photos.append(photo)


                query_ingredients = """
                    SELECT i.id, i.name FROM recipe_ingredients as ri INNER JOIN ingredient as i ON ri.id_ingredient = i.id WHERE ri.id_recipe = {0}
                    """.format(row[0])
                
                cursor.execute(query_ingredients)
                ingredients = []
                for row_ingredient in cursor.fetchall():
                    ingredient = Ingredient(id = row_ingredient[0], name = row_ingredient[1])
                    ingredients.append(ingredient)


                print("ingredients")
                print(ingredients)

                query_category = """
                    SELECT c.id, c.name FROM category as c WHERE c.id = {0}
                    """.format(row[5])
                cursor.execute(query_category)
                result_category = cursor.fetchone()
                category = Category(id = result_category[0], name = result_category[1])

                print(2)

                query_user = """
                    SELECT u.id, u.name, u.last_name, u.username FROM users as u WHERE u.id = {0}
                    """.format(row[0])
                cursor.execute(query_user)
                result_user = cursor.fetchone()
                user = User(id = result_user[0], name = result_user[1], userName = result_user[2])



                print("ingredients")
                print(ingredients)

                print("user")
                print(user)

                print("category")
                print(category)



                recipe = Reciepe(idReciepe = row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category, prepatarionTimeMinutes=row[3], idUser=row[4])
                allRecipes.append(recipe)
            return ResponseRecipes(recipes = allRecipes)

        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseRecipes(recipes = allRecipes)



    def GetUserById(self, request, context):
        try:
            query = "SELECT u.id, u.name, u.last_name, u.username, u.popularity from users as u WHERE u.id = '{0}'".format(request.id)
            cursor.execute(query)
            result = cursor.fetchone()
            if(result is None):
                return ResponseUser(id=-1)                  
            else:
                return ResponseUser(id = result[0], name = result[1], lastName = result[2], userName = result[3],popularity = result[4])                          
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseUser(id=-1)
    def GetUser(self, request, context):
        try:
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.username = '{0}' AND u.password = '{1}'".format(request.userName, request.password)
            cursor.execute(query)
            result = cursor.fetchone()
            if(result is None):
                return ResponseUser(id=-1)                  
            else:
                return ResponseUser(id = result[0], name = result[1], lastName = result[2], userName = result[3])                          
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseUser(id=-1)
    
    def RegisterUser(self, request, context):
        try:
            query = "INSERT INTO users (name, last_name, email, username, password) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}') RETURNING id;".format(request.name, request.lastName, request.email, request.userName,request.password)
            cursor.execute(query)       
            result = cursor.fetchone()
            idUser = result[0]
            print(idUser)
            db.commit()
            return Response(message = '{0}'.format(idUser))
                                    
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "-1")
    def UpdateReciepe(self, request, context):
        print("-----------------UpdateReciepe-----------------")
        print(request)
        
        try:
            query = 1
            query = "UPDATE recipes set title = '{0}', description = '{1}', isDraft = 0, preparation_time_minutes = '{2}', id_category = '{3}' WHERE id = '{4}';".format(request.title,request.description,request.prepatarionTimeMinutes,request.category.id,request.idReciepe)
            cursor.execute(query)
            
            query = "DELETE FROM recipe_photos WHERE id_recipe = '{0}';".format(request.idReciepe)
            cursor.execute(query)
            for photo in request.photos:
                query = "INSERT INTO recipe_photos (url,id_recipe) VALUES ('{0}','{1}') ;".format(photo.url,request.idReciepe)
                cursor.execute(query)

            query = "DELETE FROM recipe_steps WHERE id_recipe = '{0}'".format(request.idReciepe)
            cursor.execute(query)
            for stept in request.stepts:
                print(stept)
                query = "INSERT INTO recipe_steps (description,id_recipe) VALUES  ('{0}','{1}');".format(stept.description,request.idReciepe)
                cursor.execute(query)
            
            query = "DELETE FROM recipe_ingredients WHERE id_recipe = '{0}'".format(request.idReciepe)
            cursor.execute(query)
            for ingredient in request.ingredients:
                query = "INSERT INTO recipe_ingredients (id_ingredient,id_recipe) VALUES('{0}','{1}')".format(ingredient.id,request.idReciepe)
                cursor.execute(query)
            
            db.commit()
            return Response(message = "Recipe updated succesfully")
            
        
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "Error")
    
    def GetRecipeById(self, request, context):
        try:
            recipe_id = request.id
            query_recipe = "SELECT * FROM recipes as r WHERE r.id = '{0}'".format(recipe_id)
            cursor.execute(query_recipe)
            row = cursor.fetchone()
            #print(row)
            #if row is None:
                
             #   return ResponseRecipe(None)

            print(row)
            
            query_photos = "SELECT * FROM recipe_photos as rp WHERE rp.id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_photos)
            photos = [Photo(id=row_photo[0], url=row_photo[1]) for row_photo in cursor.fetchall()]
            print(photos)
            
            query_ingredients = "SELECT i.id, i.name FROM recipe_ingredients as ri INNER JOIN ingredient as i ON ri.id_ingredient = i.id WHERE ri.id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_ingredients)
            ingredients = [Ingredient(id=row_ingredient[0], name=row_ingredient[1]) for row_ingredient in cursor.fetchall()]
            print(ingredients)

            query_steps = "SELECT id, description FROM recipe_steps WHERE id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_steps)
            stepts = [Stept(id=row_step[0], description=row_step[1]) for row_step in cursor.fetchall()]
            
            query_category = "SELECT c.id, c.name FROM category as c WHERE c.id = '{0}'".format(row[5])
            cursor.execute(query_category)
            result_category = cursor.fetchone()
            category = Category(id=result_category[0], name=result_category[1])
            print(category)            
            
            query_user = "SELECT u.id, u.name, u.last_name, u.username FROM users as u WHERE u.id = '{0}'".format(row[4])
            cursor.execute(query_user)
            result_user = cursor.fetchone()
            user = User(id=result_user[0], name=result_user[1], userName=result_user[2])
            
            print(user)
            
            recipe = Reciepe(idReciepe=row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category,stepts = stepts, prepatarionTimeMinutes=row[3], user=user,averageRanking = row[6], popularity = row[7])
            print(recipe)
            return ResponseRecipe(recipe=recipe)
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseRecipe(recipe=None)
        
    def GetAllRecipesByUser(self, request, context):
        try:
            print("-----------------GetAllRecipesByUser-----------------")
            print(request)
            recipe_id = request.id
            query_recipe = "SELECT * FROM recipes as r WHERE r.id_user = '{0}'".format(recipe_id)
            cursor.execute(query_recipe)
            row = cursor.fetchone()
            #print(row)
            #if row is None:
                
             #   return ResponseRecipe(None)
            print("row")
            print(row)
            
            query_photos = "SELECT * FROM recipe_photos as rp WHERE rp.id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_photos)
            photos = [Photo(id=row_photo[0], url=row_photo[1]) for row_photo in cursor.fetchall()]
            print(photos)
            
            query_ingredients = "SELECT i.id, i.name FROM recipe_ingredients as ri INNER JOIN ingredient as i ON ri.id_ingredient = i.id WHERE ri.id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_ingredients)
            ingredients = [Ingredient(id=row_ingredient[0], name=row_ingredient[1]) for row_ingredient in cursor.fetchall()]
            print(ingredients)

            query_steps = "SELECT id, description FROM recipe_steps WHERE id_recipe = '{0}'".format(recipe_id)
            cursor.execute(query_steps)
            stepts = [Stept(id=row_step[0], description=row_step[1]) for row_step in cursor.fetchall()]
            
            query_category = "SELECT c.id, c.name FROM category as c WHERE c.id = '{0}'".format(row[5])
            cursor.execute(query_category)
            result_category = cursor.fetchone()
            category = Category(id=result_category[0], name=result_category[1])
            print(category)            
            
            query_user = "SELECT u.id, u.name, u.last_name, u.username FROM users as u WHERE u.id = '{0}'".format(row[4])
            cursor.execute(query_user)
            result_user = cursor.fetchone()
            user = User(id=result_user[0], name=result_user[1], userName=result_user[2])
            
            print(user)
            
            recipe = Reciepe(idReciepe=row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category,stepts = stepts, prepatarionTimeMinutes=row[3], user=user)
            print(recipe)
            return ResponseRecipe(recipe=recipe)
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseRecipe(recipe=None)
        
    def FollowUser(self,request, context):
        print("---------------FollowUser-----------------")
        print(request)
        try:
                
            query = "SELECT id_user, id_chef_user FROM user_followers WHERE id_user = '{0}' AND id_chef_user = '{1}'".format(request.idUser,request.idChefUser)
            cursor.execute(query)
            row = cursor.fetchone()
            
            if row is not None:
                return Response(message = "Follow already exists")
            
            query_follow = "INSERT INTO user_followers (id_user,id_chef_user) VALUES('{0}','{1}')".format(request.idUser,request.idChefUser)
            cursor.execute(query_follow)
            db.commit()

            # Envía un mensaje al topic PopularidadUsuario
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idChefUser)
            cursor.execute(query)
            result = cursor.fetchone()
            
            nombre_usuario = result[3]
            
            puntaje = 1
            mensaje_popularidad = {
                'nombreUsuario': nombre_usuario,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadUsuario" con los encabezados
            producer.produce(topic='PopularidadUsuario', value=mensaje_popularidad_json, headers=headers)

            producer.flush()   

            return Response(message = "Follow succesfully")
                           
             
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "Error")
        
    def UnFollowUser(self,request, context):
        print("---------------UnFollowUser-----------------")
        print(request)
        try:
            query = "SELECT id_user, id_chef_user FROM user_followers WHERE id_user = '{0}' AND id_chef_user = '{1}';".format(request.idUser,request.idChefUser)
            cursor.execute(query)
            row = cursor.fetchone()

            print("row")
            print(row)
            
            if row is None:
                return Response(message = "There is no follow")
            
            print("paso")
            query_follow = "DELETE FROM user_followers WHERE id_user = '{0}' AND id_chef_user = '{1}';".format(request.idUser,request.idChefUser)
            cursor.execute(query_follow)
            db.commit()

            # Envía un mensaje al topic PopularidadUsuario
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idChefUser)
            cursor.execute(query)
            result = cursor.fetchone()
            
            nombre_usuario = result[3]            
        
            puntaje = -1
            mensaje_popularidad = {
                'nombreUsuario': nombre_usuario,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadUsuario" con los encabezados
            producer.produce(topic='PopularidadUsuario', value=mensaje_popularidad_json, headers=headers)

            producer.flush()   

            return Response(message = "UnFollow succesfully")
                           
             
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "Error")
        
    def CommentRecipe(self,request, context):
        try:
            idUser = request.idUser
            idRecipe = request.idReciepe
            comment = request.comment
            print("comentario")
            print(idUser)

            # Envía un mensaje al topic Comentarios
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.idUser)
            cursor.execute(query)
            result = cursor.fetchone()            
            nombre_usuario = result[3]

            query = "SELECT r.title from recipes as r WHERE r.id = '{0}'".format(request.idReciepe)
            cursor.execute(query)
            result = cursor.fetchone() 
            titulo_receta = result[0]
            # Crear un diccionario con los datos del comentario
            comentario_data = {
                    "nombre_usuario": nombre_usuario,
                    "titulo_receta": titulo_receta,
                    "comentario": comment
            } 

            # Convertir el diccionario a una cadena JSON
            mensaje_comentario = json.dumps(comentario_data)

            # Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]

            # Enviar el mensaje como JSON al topic "Comentarios" con los encabezados
            producer.produce(topic='Comentarios', value=mensaje_comentario.encode('utf-8'), headers=headers)
            
            # Espera a que todos los mensajes se envíen 
            producer.flush()   

            #Mesanje para el topic "PopularidadReceta"
            puntaje = 1
            mensaje_popularidad = {
                'IdReceta': idRecipe,
                'Puntaje': puntaje
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadReceta" con los encabezados
            producer.produce(topic='PopularidadReceta', value=mensaje_popularidad_json, headers=headers)
            
            # Espera a que todos los mensajes se envíen 
            producer.flush()   

            return Response(message = "Comentario enviado con exito!")       

        
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}") 
            return Response(message = "Error")   
        
    def GetAllCommentsByRecipe(self,request, context):
        try:
            print("------GetAllComments-------")
            allComments = []
            idRecipe = request.id
            query = "SELECT rc.id, rc.id_user, rc.id_recipe, rc.comment, LEFT(rc.created_at::text, 16) FROM recipe_comments as rc WHERE id_recipe = '{0}'".format(idRecipe)
            cursor.execute(query)

            for row in cursor.fetchall():
                
                query_user = "SELECT s.username from users as s WHERE id = '{0}'".format(row[1])
                cursor.execute(query_user)
                username = cursor.fetchone()[0]
                print("Comentario " + str(row[3]))
                comment = Comment(idComment = row[0], idUser =  row[1], idRecipe = row[2] , comment = row[3] ,username = username,  timestamp = row[4])        
                allComments.append(comment)            

            print(allComments)
            return ResponseComments(comments = allComments)        

        
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}") 
            return ResponseComments(comments = allComments)   
        
    def RateRecipe(self,request, context):
        try:
            
            print("--------------RateRecipe-----------------")
            idRecipe = request.idReciepe
            idUser = request.idUser
            clasification = request.clasification
            print("id recipe " + str(idRecipe))
            print("id user " + str(idUser))
            print("clasification " + str(clasification))
            
            #Insert a la base
            query_clasification = "INSERT INTO recipe_classifications (id_recipe, id_user, clasificacion) VALUES('{0}','{1}','{2}')".format(idRecipe,idUser,clasification)
            cursor.execute(query_clasification)
            db.commit()

            query_average_ranking = "SELECT ROUND(AVG(clasificacion), 1) AS clasificacion_promedio FROM recipe_classifications WHERE id_recipe = '{0}'".format(idRecipe)
            cursor.execute(query_average_ranking)
            result = cursor.fetchone() 
            average_ranking = result[0]

            query_update_rating = "UPDATE recipes set average_ranking = '{0}' WHERE id = '{1}'".format(average_ranking,idRecipe)
            cursor.execute(query_update_rating)
            db.commit()
            
            #Mesanje para el topic "PopularidadReceta"
            mensaje_popularidad = {
                'IdReceta': idRecipe,
                'Puntaje': clasification
            }

            # Convertir el diccionario a una cadena JSON
            mensaje_popularidad_json = json.dumps(mensaje_popularidad)
        
            #Agregar la marca de tiempo como un encabezado
            fecha_hora_actual = datetime.datetime.now()
            headers = [('timestamp', str(fecha_hora_actual))]            

            # Envia el mensaje al topic "PopularidadReceta" con los encabezados
            producer.produce(topic='PopularidadReceta', value=mensaje_popularidad_json, headers=headers)
            
            # Espera a que todos los mensajes se envíen 
            producer.flush()   

            print("--------------Qualify succesfully-----------------")
            return Response(message = "Receta Calificada con éxito")       

        
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}") 
            db.rollback()
            return Response(message = "Error")  
        
    def GetTop10Users(self,request, context):
        try:
            topUsers = []
            query_top = "SELECT s.id, s.name, s.username,  s.popularity FROM users as s where s.popularity is not null order by s.popularity desc limit 5"
            cursor.execute(query_top)

            for row in cursor.fetchall():
                print(row[0])
                print(row[1])
                print(row[2])
                print(row[3])
                print("crear el objeto")
                user = User(id=row[0], name=row[1], userName=row[2] , popularity=row[3])
                print("agregar a la lista")
                topUsers.append(user)

            return ResponseUsers(users = topUsers)
        
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}") 
            return ResponseUsers(users = topUsers)  
        
    def GetTop10Recipes(self,request, context):
        try:
            alRecipes = []
            query_top = "SELECT r.id, r.title, r.popularity FROM recipes as r where r.popularity is not null order by r.popularity desc limit 5"
            cursor.execute(query_top)

            for row in cursor.fetchall():
                
                print("crear el objeto")
                recipe = Reciepe(idReciepe = row[0],title = row[1], popularity = row[2])
                print("agregar a la lista")
                alRecipes.append(recipe)

            return ResponseUsers(recipes = alRecipes)
        
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}") 
            return ResponseRecipes(recipes = alRecipes)  
        
    def GetNovedades(self,request, context):
        try:
            allNews = []
            timestamp_ms = int(time.time() * 1000)
            group_id = f'novedades-consumer-{timestamp_ms}'
            consumer_config = {
                'bootstrap.servers': 'localhost:9092',
                'group.id': group_id,
                'auto.offset.reset': 'earliest'
            }
            
            consumer = Consumer(consumer_config)
            consumer.subscribe(['Novedades'])
            data_list = []
            contador = 0
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    if(contador >4):
                        break
                    contador = contador + 1
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('Llegamos al final de la partición en Novedades')
                    else:
                        print(f'Error en el consumidor de Novedades: {msg.error().str()}')
                else:
                    mensaje = json.loads(msg.value().decode("utf-8"))
                    print(f'Mensaje recibido en Novedades: {mensaje}')
                    # Obtiene el valor del encabezado "timestamp"
                    headers = msg.headers()
                    timestamp = None
                    for header in headers:
                        if header[0] == "timestamp":
                            timestamp = header[1].decode("utf-8")
                            break
                    if timestamp is not None:
                        # Crea un diccionario JSON con los datos
                        data = {
                            "Usuario": mensaje["Usuario"],
                            "title": mensaje["title"],
                            "URL Foto": mensaje["URL Foto"],
                            "timestamp": timestamp
                        }
                        # Agrega el diccionario a la lista
                        data_list.append(data)
                        # Ordena la lista por timestamp de mayor a menor
                        data_list = sorted(data_list, key=lambda x: x["timestamp"], reverse=True)
                
                        # Limita la lista a los 5 datos más recientes
                        data_list = data_list[:5]




            
    


            
            for data in data_list:
                novedad = Novedad(user = data["Usuario"],title = data["title"], url = data["URL Foto"])
                allNews.append(novedad)

            return ResponseNovedades(novedades = allNews)
        
        except BaseException as error:

            print(f"Unexpected {error=}, {type(error)=}") 
            return ResponseNovedades(novedades = allNews)  


def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ChefEnCasaServicer_to_server(ServiceChefEnCasa(),server)
    server.add_insecure_port('[::]:50051')
    print("Servidor escuchando en 50051!")
    server.start()
    server.wait_for_termination()
    pass


if __name__ == "__main__":
    start()