# OSS相关缓存
CACHE_OSS = 'sniper_oss'


def create_key(scope, key):
    return scope + '_' + str(key)
