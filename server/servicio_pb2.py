# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: servicio.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eservicio.proto\x12\nChefEnCasa\"\x07\n\x05\x45mpty\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t\"h\n\x13RequestRegisterUser\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08lastName\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x10\n\x08userName\x18\x04 \x01(\t\x12\x10\n\x08password\x18\x05 \x01(\t\"4\n\x0eRequestGetUser\x12\x10\n\x08userName\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"L\n\x0cResponseUser\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08lastName\x18\x03 \x01(\t\x12\x10\n\x08userName\x18\x04 \x01(\t\" \n\x05Photo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0b\n\x03url\x18\x02 \x01(\t\"&\n\nIngredient\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"B\n\x13ResponseIngredients\x12+\n\x0bingredients\x18\x01 \x03(\x0b\x32\x16.ChefEnCasa.Ingredient\"(\n\x05Stept\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"$\n\x08\x43\x61tegory\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"<\n\x11ResponseCategorys\x12\'\n\tcategorys\x18\x01 \x03(\x0b\x32\x14.ChefEnCasa.Category\"\x85\x02\n\x14RequestCreateReciepe\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12!\n\x06photos\x18\x03 \x03(\x0b\x32\x11.ChefEnCasa.Photo\x12+\n\x0bingredients\x18\x04 \x03(\x0b\x32\x16.ChefEnCasa.Ingredient\x12&\n\x08\x63\x61tegory\x18\x05 \x01(\x0b\x32\x14.ChefEnCasa.Category\x12!\n\x06stepts\x18\x06 \x03(\x0b\x32\x11.ChefEnCasa.Stept\x12\x1e\n\x16prepatarionTimeMinutes\x18\x07 \x01(\x05\x12\x0e\n\x06idUser\x18\x08 \x01(\x05\"\x1b\n\rRequestByUser\x12\n\n\x02id\x18\x01 \x01(\x05\"7\n\x0fResponseRecipes\x12$\n\x07recipes\x18\x01 \x03(\x0b\x32\x13.ChefEnCasa.Reciepe\">\n\x19RequestReciepeToFavorites\x12\x0e\n\x06idUser\x18\x01 \x01(\x05\x12\x11\n\tidReciepe\x18\x02 \x01(\x05\"\x9b\x02\n\x07Reciepe\x12\x11\n\tidReciepe\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12!\n\x06photos\x18\x04 \x03(\x0b\x32\x11.ChefEnCasa.Photo\x12+\n\x0bingredients\x18\x05 \x03(\x0b\x32\x16.ChefEnCasa.Ingredient\x12&\n\x08\x63\x61tegory\x18\x06 \x01(\x0b\x32\x14.ChefEnCasa.Category\x12!\n\x06stepts\x18\x07 \x03(\x0b\x32\x11.ChefEnCasa.Stept\x12\x1e\n\x16prepatarionTimeMinutes\x18\x08 \x01(\x05\x12\x1e\n\x04user\x18\t \x01(\x0b\x32\x10.ChefEnCasa.User\"7\n\x11RequestFollowUser\x12\x0e\n\x06idUser\x18\x01 \x01(\x05\x12\x12\n\nidChefUser\x18\x02 \x01(\x05\"2\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08userName\x18\x03 \x01(\t\"0\n\rResponseUsers\x12\x1f\n\x05users\x18\x01 \x03(\x0b\x32\x10.ChefEnCasa.User\"\xc7\x01\n\x1bRequestGetRecipiesByFilters\x12&\n\x08\x63\x61tegory\x18\x01 \x01(\x0b\x32\x14.ChefEnCasa.Category\x12\r\n\x05title\x18\x02 \x01(\t\x12+\n\x0bingredients\x18\x03 \x03(\x0b\x32\x16.ChefEnCasa.Ingredient\x12!\n\x19prepatarionTimeMinutesMin\x18\x04 \x01(\x05\x12!\n\x19prepatarionTimeMinutesMax\x18\x05 \x01(\x05\"9\n\x10ResponseRecipies\x12%\n\x08recipies\x18\x01 \x03(\x0b\x32\x13.ChefEnCasa.Reciepe\"\x88\x02\n\x14RequestUpdateReciepe\x12\x11\n\tidReciepe\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12!\n\x06photos\x18\x04 \x03(\x0b\x32\x11.ChefEnCasa.Photo\x12+\n\x0bingredients\x18\x05 \x03(\x0b\x32\x16.ChefEnCasa.Ingredient\x12&\n\x08\x63\x61tegory\x18\x06 \x01(\x0b\x32\x14.ChefEnCasa.Category\x12!\n\x06stepts\x18\x07 \x03(\x0b\x32\x11.ChefEnCasa.Stept\x12\x1e\n\x16prepatarionTimeMinutes\x18\x08 \x01(\x05\x32\xf8\x08\n\nChefEnCasa\x12?\n\x07GetUser\x12\x1a.ChefEnCasa.RequestGetUser\x1a\x18.ChefEnCasa.ResponseUser\x12\x42\n\x0bGetUserById\x12\x19.ChefEnCasa.RequestByUser\x1a\x18.ChefEnCasa.ResponseUser\x12?\n\rGetAllRecipes\x12\x11.ChefEnCasa.Empty\x1a\x1b.ChefEnCasa.ResponseRecipes\x12M\n\x13GetAllRecipesByUser\x12\x19.ChefEnCasa.RequestByUser\x1a\x1b.ChefEnCasa.ResponseRecipes\x12R\n\x17GetAllFavoritesReciepes\x12\x19.ChefEnCasa.RequestByUser\x1a\x1c.ChefEnCasa.ResponseRecipies\x12J\n\x12GetAllSuscriptions\x12\x19.ChefEnCasa.RequestByUser\x1a\x19.ChefEnCasa.ResponseUsers\x12]\n\x14GetRecipiesByFilters\x12\'.ChefEnCasa.RequestGetRecipiesByFilters\x1a\x1c.ChefEnCasa.ResponseRecipies\x12G\n\x11GetAllIngredients\x12\x11.ChefEnCasa.Empty\x1a\x1f.ChefEnCasa.ResponseIngredients\x12\x43\n\x0fGetAllCategorys\x12\x11.ChefEnCasa.Empty\x1a\x1d.ChefEnCasa.ResponseCategorys\x12\x45\n\x0cRegisterUser\x12\x1f.ChefEnCasa.RequestRegisterUser\x1a\x14.ChefEnCasa.Response\x12\x46\n\x0c\x43reateRecipe\x12 .ChefEnCasa.RequestCreateReciepe\x1a\x14.ChefEnCasa.Response\x12T\n\x15\x41\x64\x64ReciepeToFavorites\x12%.ChefEnCasa.RequestReciepeToFavorites\x1a\x14.ChefEnCasa.Response\x12W\n\x18RemoveReciepeToFavorites\x12%.ChefEnCasa.RequestReciepeToFavorites\x1a\x14.ChefEnCasa.Response\x12\x41\n\nFollowUser\x12\x1d.ChefEnCasa.RequestFollowUser\x1a\x14.ChefEnCasa.Response\x12G\n\rUpdateReciepe\x12 .ChefEnCasa.RequestUpdateReciepe\x1a\x14.ChefEnCasa.Responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'servicio_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EMPTY']._serialized_start=30
  _globals['_EMPTY']._serialized_end=37
  _globals['_RESPONSE']._serialized_start=39
  _globals['_RESPONSE']._serialized_end=66
  _globals['_REQUESTREGISTERUSER']._serialized_start=68
  _globals['_REQUESTREGISTERUSER']._serialized_end=172
  _globals['_REQUESTGETUSER']._serialized_start=174
  _globals['_REQUESTGETUSER']._serialized_end=226
  _globals['_RESPONSEUSER']._serialized_start=228
  _globals['_RESPONSEUSER']._serialized_end=304
  _globals['_PHOTO']._serialized_start=306
  _globals['_PHOTO']._serialized_end=338
  _globals['_INGREDIENT']._serialized_start=340
  _globals['_INGREDIENT']._serialized_end=378
  _globals['_RESPONSEINGREDIENTS']._serialized_start=380
  _globals['_RESPONSEINGREDIENTS']._serialized_end=446
  _globals['_STEPT']._serialized_start=448
  _globals['_STEPT']._serialized_end=488
  _globals['_CATEGORY']._serialized_start=490
  _globals['_CATEGORY']._serialized_end=526
  _globals['_RESPONSECATEGORYS']._serialized_start=528
  _globals['_RESPONSECATEGORYS']._serialized_end=588
  _globals['_REQUESTCREATERECIEPE']._serialized_start=591
  _globals['_REQUESTCREATERECIEPE']._serialized_end=852
  _globals['_REQUESTBYUSER']._serialized_start=854
  _globals['_REQUESTBYUSER']._serialized_end=881
  _globals['_RESPONSERECIPES']._serialized_start=883
  _globals['_RESPONSERECIPES']._serialized_end=938
  _globals['_REQUESTRECIEPETOFAVORITES']._serialized_start=940
  _globals['_REQUESTRECIEPETOFAVORITES']._serialized_end=1002
  _globals['_RECIEPE']._serialized_start=1005
  _globals['_RECIEPE']._serialized_end=1288
  _globals['_REQUESTFOLLOWUSER']._serialized_start=1290
  _globals['_REQUESTFOLLOWUSER']._serialized_end=1345
  _globals['_USER']._serialized_start=1347
  _globals['_USER']._serialized_end=1397
  _globals['_RESPONSEUSERS']._serialized_start=1399
  _globals['_RESPONSEUSERS']._serialized_end=1447
  _globals['_REQUESTGETRECIPIESBYFILTERS']._serialized_start=1450
  _globals['_REQUESTGETRECIPIESBYFILTERS']._serialized_end=1649
  _globals['_RESPONSERECIPIES']._serialized_start=1651
  _globals['_RESPONSERECIPIES']._serialized_end=1708
  _globals['_REQUESTUPDATERECIEPE']._serialized_start=1711
  _globals['_REQUESTUPDATERECIEPE']._serialized_end=1975
  _globals['_CHEFENCASA']._serialized_start=1978
  _globals['_CHEFENCASA']._serialized_end=3122
# @@protoc_insertion_point(module_scope)
