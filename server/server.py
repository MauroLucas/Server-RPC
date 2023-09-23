from servicio_pb2_grpc import ChefEnCasaServicer, add_ChefEnCasaServicer_to_server
from servicio_pb2 import ResponseUser, ResponseIngredients, Ingredient, Category , ResponseCategorys, ResponseRecipes, Reciepe,Photo, User, Response, ResponseRecipe, Stept

import grpc
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

cursor = db.cursor();

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
            return Response(message = '{0}'.format(idRecipe))
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            db.rollback()
            return Response(message = "-1")
    def AddReciepeToFavorites(self, request, context):
        print("like")
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
            SELECT * FROM recipes as r where r.id in (SELECT id_recipe FROM user_favorite_recipes as ufr WHERE ufr.id_user = {0})
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
        print(request)
        print(type(request))

        allRecipes = []

        try:
            # preparation_time_minutes lower than
            # title contains
            query_recipes = """
                SELECT * FROM recipes as r where r.id_category = {0} and title like '%{1}%' and r.preparation_time_minutes <= {2}
            """.format(request.category.id, request.title.lower(), request.prepatarionTimeMinutesMax)

            print("catId")
            print(request.category.id)

            if (request.category.id == 0):
                query_recipes = """
                    SELECT * FROM recipes as r where lower(title) like '%{0}%' and r.preparation_time_minutes <= {1}
                """.format(request.title.lower(), request.prepatarionTimeMinutesMax)
                if (request.title == "."):
                    query_recipes = """
                        SELECT * FROM recipes as r where r.preparation_time_minutes <= {0}
                    """.format(request.prepatarionTimeMinutesMax)
            if (request.title == "." and request.category.id != 0):
                query_recipes = """
                    SELECT * FROM recipes as r where r.id_category = {0}
                """.format(request.category.id)

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
            query = "SELECT u.id, u.name, u.last_name, u.username from users as u WHERE u.id = '{0}'".format(request.id)
            cursor.execute(query)
            result = cursor.fetchone()
            if(result is None):
                return ResponseUser(id=-1)                  
            else:
                return ResponseUser(id = result[0], name = result[1], lastName = result[2], userName = result[3])                          
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
        try:
            query = 1
            query = "UPDATE recipes set title = '{0}', description = '{1}', preparation_time_minutes = '{2}', id_category = '{3}' WHERE id = '{4}';".format(request.title,request.description,request.prepatarionTimeMinutes,request.category.id,request.idReciepe)
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
            
            recipe = Reciepe(idReciepe=row[0], title=row[1], description=row[2], photos=photos, ingredients=ingredients, category=category,stepts = stepts, prepatarionTimeMinutes=row[3], user=user)
            print(recipe)
            return ResponseRecipe(recipe=recipe)
        except BaseException as error:
            print(f"Unexpected {error=}, {type(error)=}")
            return ResponseRecipe(recipe=None)
        
          
        

        

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