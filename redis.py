# import functools
# import json
# # from flask import Response, current_app, request
# from fastapi import Response,request

# import redis
# from redis.commands.json.path import Path


# def get_current_cache_key():
#     return current_app.config['APP_NAME'] + ':' + request.full_path.strip('?')


# def update_cache(key: str, value: dict):
#     redis_client = redis.from_url(current_app.config["REDIS_URI"])
#     redis_cache_duration = current_app.config["REDIS_CACHE_EXPIRES"]

#     redis_client.json().set(key, Path.root_path(), value)
#     if value:
#         redis_client.expire(key, redis_cache_duration)
#     else:
#         redis_client.expire(key, 0)


# def get_from_cache(key: str):
#     redis_client = redis.from_url(current_app.config["REDIS_URI"])
#     return redis_client.json().get(key)


# def update_cache_from_endpoint_result(cache_key, endpoint_result):
#     # current_app.logger.info(type(endpoint_result))
#     if isinstance(endpoint_result, dict):
#         # current_app.logger.debug(endpoint_result)
#         update_cache(cache_key, endpoint_result)

#     elif isinstance(endpoint_result, tuple):
#         # current_app.logger.debug(endpoint_result[1])
#         # current_app.logger.debug(type(endpoint_result[0]))
#         # current_app.logger.debug(endpoint_result[0])
#         update_cache(cache_key, endpoint_result[0])

#     elif isinstance(endpoint_result, Response) and endpoint_result.status_code//100 == 2:
#         # current_app.logger.debug(endpoint_result.status_code)
#         # current_app.logger.debug(endpoint_result.data)
#         update_cache(cache_key, json.loads(endpoint_result.data.decode()))

#     else:
#         # current_app.logger.debug(endpoint_result.status_code)
#         # current_app.logger.debug(endpoint_result.data)
#         raise redis.exceptions.RedisError("Can't update the result to RedisCache. Unknown Response Type found! " + str(type(endpoint_result)))

# def get_id_from_result(endpoint_result):
#     if isinstance(endpoint_result, dict):
#         return str(endpoint_result['id'])
    
#     elif isinstance(endpoint_result, tuple):
#         return str(endpoint_result[0]['id'])

#     elif isinstance(endpoint_result, Response) and endpoint_result.status_code//100 == 2:
#         res = endpoint_result.data.decode()
#         res = json.loads(res)
#         return str(res['id'])
#     else:
#         raise redis.exceptions.RedisError("Can't add the result to RedisCache. Unknown Response Type found! " + str(type(endpoint_result)))
    

# def redis_cache_get(_func=None, *, access_type=["1"]):
#     def fn_wrapper(func):
#         @functools.wraps(func)
#         def args_wrapper(*args, **kwargs):
#             try:
#                 cache_key = get_current_cache_key()
#                 result = get_from_cache(cache_key)
#                 if result:
#                     current_app.logger.info('result from cache')
#                     return result
#                 else:
#                     current_app.logger.info('result from api endpoint')

#                     endpoint_result = func(*args, **kwargs)
#                     update_cache_from_endpoint_result(cache_key, endpoint_result)
#                     return endpoint_result
#             except redis.exceptions.RedisError:
#                 current_app.logger.warning('redis cache exception occurred while reading a key: ' + cache_key)
#                 return func(*args, **kwargs)
#         return args_wrapper

#     if _func is not None:
#         return fn_wrapper(_func)
#     else:
#         return fn_wrapper


# def redis_cache_update(_func=None, *, access_type=["1"]):
#     def fn_wrapper(func):
#         @functools.wraps(func)
#         def args_wrapper(*args, **kwargs):
#             cache_key = get_current_cache_key()
#             endpoint_result = func(*args, **kwargs)
            
#             try:
#                 update_cache_from_endpoint_result(cache_key, endpoint_result)
#                 current_app.logger.info('cache updated')
#             except redis.exceptions.RedisError:
#                 current_app.logger.warning('redis cache exception occurred while updating a key: ' + cache_key)

#             return endpoint_result
#         return args_wrapper

#     if _func is not None:
#         return fn_wrapper(_func)
#     else:
#         return fn_wrapper


# def redis_cache_delete(_func=None, *, access_type=["1"]):
#     def fn_wrapper(func):
#         @functools.wraps(func)
#         def args_wrapper(*args, **kwargs):
#             cache_key = get_current_cache_key()

#             try:
#                 update_cache(cache_key, None)
#                 current_app.logger.info('cache deleted')
#             except redis.exceptions.RedisError:
#                 current_app.logger.warning('redis cache exception occurred while deleteing the key: ' + cache_key)

#             return func(*args, **kwargs)

#         return args_wrapper

#     if _func is not None:
#         return fn_wrapper(_func)
#     else:
#         return fn_wrapper


# def redis_cache_add(_func=None, *, access_type=["1"]):
#     def fn_wrapper(func):
#         @functools.wraps(func)
#         def args_wrapper(*args, **kwargs):
#             cache_key = get_current_cache_key()
#             endpoint_result = func(*args, **kwargs)
#             cache_key = cache_key + get_id_from_result(endpoint_result)

#             try:
#                 update_cache_from_endpoint_result(cache_key, endpoint_result)
#                 current_app.logger.info('cache added')
#             except redis.exceptions.RedisError:
#                 current_app.logger.warning('redis cache: exception occurred while adding a new key: ' + cache_key)

#             return endpoint_result
#         return args_wrapper

#     if _func is not None:
#         return fn_wrapper(_func)
#     else:
#         return fn_wrapper