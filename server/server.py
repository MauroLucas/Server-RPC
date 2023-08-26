from servicio_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from servicio_pb2 import HelloReply

import grpc
from concurrent import futures

class ServicioGreet(GreeterServicer):
    def SayHello(self, request, context):
        return HelloReply(message = (f"Hola {request.name}!"))

def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(ServicioGreet(),server)
    server.add_insecure_port('[::]:50051')
    print("Servidor escuchando en 50051!")
    server.start()
    server.wait_for_termination()
    pass


if __name__ == "__main__":
    start()