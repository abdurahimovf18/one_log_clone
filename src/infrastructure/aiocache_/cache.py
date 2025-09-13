
### TODO: After business logic is done, cache should be added




# import asyncio

# from aiocache import caches, Cache
# from aiocache.serializers import StringSerializer, PickleSerializer


# def set_cache_config():

#     caches.set_config({
#         'default': {
#             'cache': "aiocache.RedisCache",
#             'endpoint': "127.0.0.1",
#             'port': 6379,
#             'timeout': 1,
#             'serializer': {
#                 'class': "src.infrastructure.aiocache_._orjson_serializer.OrjsonSerializer"
#             }
#         },
#         'redis_alt': {
#             'cache': "aiocache.RedisCache",

#             'plugins': [
#                 {'class': "aiocache.plugins.HitMissRatioPlugin"},
#                 {'class': "aiocache.plugins.TimingPlugin"}
#             ]
#         }
#     })


# async def default_cache():
#     cache = caches.get('default')   # This always returns the same instance
#     await cache.set("key", "value")

#     assert await cache.get("key") == "value"
#     assert isinstance(cache, Cache.MEMORY)
#     assert isinstance(cache.serializer, StringSerializer)


# async def alt_cache():
#     # This generates a new instance every time! You can also use
#     # `caches.create("alt", namespace="test", etc...)` to override extra args
#     cache = caches.create("redis_alt")
#     await cache.set("key", "value")

#     assert await cache.get("key") == "value"
#     assert isinstance(cache, Cache.REDIS)
#     assert isinstance(cache.serializer, PickleSerializer)
#     assert len(cache.plugins) == 2
#     assert cache.endpoint == "127.0.0.1"
#     assert cache.timeout == 1
#     assert cache.port == 6379
#     await cache.close()


# async def test_alias():
#     await default_cache()
#     await alt_cache()

#     cache = Cache(Cache.REDIS)
#     await cache.delete("key")
#     await cache.close()

#     await caches.get("default").close()


# if __name__ == "__main__":
#     asyncio.run(test_alias())




# # {
# #     "versions": {
# #         "id<uuid>": {
# #             "transaction": {
# #                 "commited": True
# #             },
# #             "metadata": {
# #                 "values": {
# #                     "id": "uuid",
# #                     "name": "..."
# #                 }
# #             }
# #         }
# #     }
# # }
