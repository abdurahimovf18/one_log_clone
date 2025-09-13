# from aiocache.serializers import BaseSerializer
# from orjson import dumps, loads


# class OrjsonSerializer(BaseSerializer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def dumps(self, value: object) -> bytes:  # type: ignore
#         return dumps(value)

#     def loads(self, value: bytes | None) -> object:  # type: ignore
#         if value is None:
#             return None
#         return loads(value)
    
        
