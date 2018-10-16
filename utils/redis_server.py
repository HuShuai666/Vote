# coding: utf-8
import redis
from Vote.settings import REDIS_CONFIG

redis_valid_time = 60 * 60


class RedisClient:

    @property
    def redis_client(self):
        pool = redis.ConnectionPool(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
        client = redis.Redis(connection_pool=pool)
        return client

    def exist_key(self, key):
        """根据key判断元素是否存在缓存中"""
        return self.redis_client.exists(key)

    def get_instance(self, key, delete_cache=False):
        """根据key获取value（string类型数据操作）"""
        redis_instance = self.redis_client.get(key)
        if not redis_instance:
            return None
        try:
            res = eval(redis_instance)
        except:
            res = str(redis_instance, encoding='utf-8')
        if delete_cache:
            self.redis_client.delete(key)
        return res

    def set_instance(self, key, value, default_valid_time=redis_valid_time):
        """设置键值对（string类型数据操作）"""
        self.redis_client.set(key, value, default_valid_time)
        return

    def delete(self, key):
        """删除键值对（string类型数据操作）"""
        self.redis_client.delete(key)
        return

    def incr_instance(self, key, amount=1):
        """根据key自增amount（string类型数据操作）"""
        self.redis_client.incr(key, amount)
        return

    def decr_instance(self, key, amount=1):
        """根据key自减amount（string类型数据操作）"""
        self.redis_client.decr(key, amount)
        return

    def sadd(self, name, *value):
        """根据key添加数据到集合set（set类型数据操作）"""
        self.redis_client.sadd(name, *value)
        return

    def sismember(self, name, value):
        """判断集合name中是否存在value元素（set类型数据操作）"""
        return self.redis_client.sismember(name, value)

    def smembers(self, name):
        """返回集合name中所有元素（set类型数据操作）"""
        return self.redis_client.smembers(name)

    def scard(self, name):
        """返回集合name中元素个数（set类型数据操作）"""
        return self.redis_client.scard(name)

    def spop(self, name):
        """从集合右侧返回并移除一个成员（set类型数据操作）"""
        return self.redis_client.spop(name)

    def srandmember(self, name, numbers):
        """从name对应的集合中随机获取numbers个元素（set类型数据操作）"""
        data_list = self.redis_client.srandmember(name, numbers)
        return [str(data, encoding='utf-8') for data in data_list]

    def srem(self, name, values):
        """在name对应的集合中删除某些值（set类型数据操作）"""
        return self.redis_client.srem(name, values)

    def zadd(self, name, *args, **kwargs):
        self.redis_client.zadd(name, *args, **kwargs)

    def zrange(self, name, start, stop):
        self.redis_client.zrange(name, start, stop, withscores=True)

    def hset(self, name, key, value):
        """在name对应的集合中添加某些值（hash类型数据操作）"""
        return self.redis_client.hset(name, key, value)

    def hmset(self, name, mapping):
        """在name对应的集合中批量添加某些值（hash类型数据操作）"""
        return self.redis_client.hmset(name, mapping)

    def hget(self, name, key):
        """在name对应的集合中获取key的元素（hash类型数据操作）"""
        return self.redis_client.hget(name, key)

    def hmget(self, name, keys, *args):
        """在name对应的集合中批量获取元素（hash类型数据操作）"""
        return self.redis_client.hmget(name, keys, *args)


redis_client = RedisClient()
