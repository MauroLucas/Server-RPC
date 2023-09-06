from servicio_pb2_grpc import ChefEnCasaServicer, add_ChefEnCasaServicer_to_server
from servicio_pb2 import ResponseUser, ResponseIngredients, Ingredient, Category , ResponseCategorys, ResponseRecipes, Reciepe,Photo, User

import grpc
from concurrent import futures

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database = "chefencasa"
)
db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

cursor = db.cursor();

class ServiceChefEnCasa(ChefEnCasaServicer):
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
                    """.format(row[0])
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