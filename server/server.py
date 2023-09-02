from servicio_pb2_grpc import ChefEnCasaServicer, add_ChefEnCasaServicer_to_server
from servicio_pb2 import ResponseUser

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