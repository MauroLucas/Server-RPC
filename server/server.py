from servicio_pb2_grpc import ChefEnCasaServicer, add_ChefEnCasaServicer_to_server
from servicio_pb2 import ResponseUser

import grpc
from concurrent import futures

class ServiceChefEnCasa(ChefEnCasaServicer):
    def GetUser(self, request, context):
        print(request.userName)
        print(request.password)
        return ResponseUser(id = 1, name = "Mauro" , lastName = "Pereyra" , userName = f"{request.userName}")

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