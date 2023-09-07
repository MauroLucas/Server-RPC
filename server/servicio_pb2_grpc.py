# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import servicio_pb2 as servicio__pb2


class ChefEnCasaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUser = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetUser',
                request_serializer=servicio__pb2.RequestGetUser.SerializeToString,
                response_deserializer=servicio__pb2.ResponseUser.FromString,
                )
        self.GetUserById = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetUserById',
                request_serializer=servicio__pb2.RequestByUser.SerializeToString,
                response_deserializer=servicio__pb2.ResponseUser.FromString,
                )
        self.GetAllRecipes = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllRecipes',
                request_serializer=servicio__pb2.Empty.SerializeToString,
                response_deserializer=servicio__pb2.ResponseRecipes.FromString,
                )
        self.GetAllRecipesByUser = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllRecipesByUser',
                request_serializer=servicio__pb2.RequestByUser.SerializeToString,
                response_deserializer=servicio__pb2.ResponseRecipes.FromString,
                )
        self.GetAllFavoritesReciepes = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllFavoritesReciepes',
                request_serializer=servicio__pb2.RequestByUser.SerializeToString,
                response_deserializer=servicio__pb2.ResponseRecipies.FromString,
                )
        self.GetAllSuscriptions = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllSuscriptions',
                request_serializer=servicio__pb2.RequestByUser.SerializeToString,
                response_deserializer=servicio__pb2.ResponseUsers.FromString,
                )
        self.GetRecipiesByFilters = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetRecipiesByFilters',
                request_serializer=servicio__pb2.RequestGetRecipiesByFilters.SerializeToString,
                response_deserializer=servicio__pb2.ResponseRecipies.FromString,
                )
        self.GetAllIngredients = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllIngredients',
                request_serializer=servicio__pb2.Empty.SerializeToString,
                response_deserializer=servicio__pb2.ResponseIngredients.FromString,
                )
        self.GetAllCategorys = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/GetAllCategorys',
                request_serializer=servicio__pb2.Empty.SerializeToString,
                response_deserializer=servicio__pb2.ResponseCategorys.FromString,
                )
        self.RegisterUser = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/RegisterUser',
                request_serializer=servicio__pb2.RequestRegisterUser.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )
        self.CreateRecipe = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/CreateRecipe',
                request_serializer=servicio__pb2.RequestCreateReciepe.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )
        self.AddReciepeToFavorites = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/AddReciepeToFavorites',
                request_serializer=servicio__pb2.RequestReciepeToFavorites.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )
        self.RemoveReciepeToFavorites = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/RemoveReciepeToFavorites',
                request_serializer=servicio__pb2.RequestReciepeToFavorites.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )
        self.FollowUser = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/FollowUser',
                request_serializer=servicio__pb2.RequestFollowUser.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )
        self.UpdateReciepe = channel.unary_unary(
                '/ChefEnCasa.ChefEnCasa/UpdateReciepe',
                request_serializer=servicio__pb2.RequestUpdateReciepe.SerializeToString,
                response_deserializer=servicio__pb2.Response.FromString,
                )


class ChefEnCasaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllRecipes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllRecipesByUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllFavoritesReciepes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllSuscriptions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRecipiesByFilters(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllIngredients(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllCategorys(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRecipe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddReciepeToFavorites(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveReciepeToFavorites(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FollowUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateReciepe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChefEnCasaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=servicio__pb2.RequestGetUser.FromString,
                    response_serializer=servicio__pb2.ResponseUser.SerializeToString,
            ),
            'GetUserById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserById,
                    request_deserializer=servicio__pb2.RequestByUser.FromString,
                    response_serializer=servicio__pb2.ResponseUser.SerializeToString,
            ),
            'GetAllRecipes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllRecipes,
                    request_deserializer=servicio__pb2.Empty.FromString,
                    response_serializer=servicio__pb2.ResponseRecipes.SerializeToString,
            ),
            'GetAllRecipesByUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllRecipesByUser,
                    request_deserializer=servicio__pb2.RequestByUser.FromString,
                    response_serializer=servicio__pb2.ResponseRecipes.SerializeToString,
            ),
            'GetAllFavoritesReciepes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllFavoritesReciepes,
                    request_deserializer=servicio__pb2.RequestByUser.FromString,
                    response_serializer=servicio__pb2.ResponseRecipies.SerializeToString,
            ),
            'GetAllSuscriptions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllSuscriptions,
                    request_deserializer=servicio__pb2.RequestByUser.FromString,
                    response_serializer=servicio__pb2.ResponseUsers.SerializeToString,
            ),
            'GetRecipiesByFilters': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRecipiesByFilters,
                    request_deserializer=servicio__pb2.RequestGetRecipiesByFilters.FromString,
                    response_serializer=servicio__pb2.ResponseRecipies.SerializeToString,
            ),
            'GetAllIngredients': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllIngredients,
                    request_deserializer=servicio__pb2.Empty.FromString,
                    response_serializer=servicio__pb2.ResponseIngredients.SerializeToString,
            ),
            'GetAllCategorys': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllCategorys,
                    request_deserializer=servicio__pb2.Empty.FromString,
                    response_serializer=servicio__pb2.ResponseCategorys.SerializeToString,
            ),
            'RegisterUser': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterUser,
                    request_deserializer=servicio__pb2.RequestRegisterUser.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
            'CreateRecipe': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateRecipe,
                    request_deserializer=servicio__pb2.RequestCreateReciepe.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
            'AddReciepeToFavorites': grpc.unary_unary_rpc_method_handler(
                    servicer.AddReciepeToFavorites,
                    request_deserializer=servicio__pb2.RequestReciepeToFavorites.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
            'RemoveReciepeToFavorites': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveReciepeToFavorites,
                    request_deserializer=servicio__pb2.RequestReciepeToFavorites.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
            'FollowUser': grpc.unary_unary_rpc_method_handler(
                    servicer.FollowUser,
                    request_deserializer=servicio__pb2.RequestFollowUser.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
            'UpdateReciepe': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateReciepe,
                    request_deserializer=servicio__pb2.RequestUpdateReciepe.FromString,
                    response_serializer=servicio__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChefEnCasa.ChefEnCasa', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChefEnCasa(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetUser',
            servicio__pb2.RequestGetUser.SerializeToString,
            servicio__pb2.ResponseUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUserById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetUserById',
            servicio__pb2.RequestByUser.SerializeToString,
            servicio__pb2.ResponseUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllRecipes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllRecipes',
            servicio__pb2.Empty.SerializeToString,
            servicio__pb2.ResponseRecipes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllRecipesByUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllRecipesByUser',
            servicio__pb2.RequestByUser.SerializeToString,
            servicio__pb2.ResponseRecipes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllFavoritesReciepes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllFavoritesReciepes',
            servicio__pb2.RequestByUser.SerializeToString,
            servicio__pb2.ResponseRecipies.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllSuscriptions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllSuscriptions',
            servicio__pb2.RequestByUser.SerializeToString,
            servicio__pb2.ResponseUsers.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRecipiesByFilters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetRecipiesByFilters',
            servicio__pb2.RequestGetRecipiesByFilters.SerializeToString,
            servicio__pb2.ResponseRecipies.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllIngredients(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllIngredients',
            servicio__pb2.Empty.SerializeToString,
            servicio__pb2.ResponseIngredients.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllCategorys(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/GetAllCategorys',
            servicio__pb2.Empty.SerializeToString,
            servicio__pb2.ResponseCategorys.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/RegisterUser',
            servicio__pb2.RequestRegisterUser.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateRecipe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/CreateRecipe',
            servicio__pb2.RequestCreateReciepe.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddReciepeToFavorites(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/AddReciepeToFavorites',
            servicio__pb2.RequestReciepeToFavorites.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveReciepeToFavorites(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/RemoveReciepeToFavorites',
            servicio__pb2.RequestReciepeToFavorites.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FollowUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/FollowUser',
            servicio__pb2.RequestFollowUser.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateReciepe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChefEnCasa.ChefEnCasa/UpdateReciepe',
            servicio__pb2.RequestUpdateReciepe.SerializeToString,
            servicio__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
