import redis
import uuid
import time
import math
import copy

try:
    import bitarray
except ImportError:
    raise ImportError('Requires bitarray')
try:
    import mmh3
except ImportError:
    raise ImportError('Requires mmh3')

def acquire_lock_with_timeout(conn, lockname, acquire_timeout=5, lock_timeout=10):
    # 128位随机标识符
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))  # 确保传给exprie是整数

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):
            conn.expire(lockname, lock_timeout)
            return identifier
        elif not conn.ttl(lockname):  # 为没有设置超时时间的锁设置超时时间
            conn.expire(lockname, lock_timeout)

        time.sleep(0.001)
    return False


# 释放锁
def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname

    while True:
        try:
            pipe.watch(lockname)
            # 判断标志是否相同
            if str(pipe.get(lockname), encoding='utf-8') == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True

            # 不同则直接退出 return False
            pipe.unwatch()
            break

        except redis.exceptions.WatchError:
            pass
    return False

class BloomFilter(object):

    def __init__(self, data_size, error_rate=0.001):
        """
        :param data_size: 所需存放数据的数量
        :param error_rate:  可接受的误报率，默认0.001
        通过这两个参数来确定需要多少个哈希函数以及位数组的大小
        >>> bf = BloomFilter(data_size=100000, error_rate=0.001)
        >>> bf.add("test")
        True
        >>> "test" in bf
        True
        """

        if not data_size > 0:
            raise ValueError("Capacity must be > 0")
        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")

        self.data_size = data_size
        self.error_rate = error_rate

        bit_num, hash_num = self._adjust_param(data_size, error_rate)
        self._bit_array = bitarray.bitarray(bit_num)
        self._bit_array.setall(0)
        self._bit_num = bit_num
        self._hash_num = hash_num

        # 将哈希种子固定为 1 - hash_num （预留持久化过滤的可能）
        self._hash_seed = [i for i in range(1, hash_num+1)]

        # 已存数据量
        self._data_count = 0

    def add(self, key):
        """
        :param key: 要添加的数据
        :return:
        >>> bf = BloomFilter(data_size=100000, error_rate=0.001)
        >>> bf.add("test")
        True
        """
        if self._is_half_fill():
            raise IndexError("The capacity is insufficient")

        for time in range(self._hash_num):
            key_hashed_idx = mmh3.hash(key, self._hash_seed[time]) % self._bit_num
            self._bit_array[key_hashed_idx] = 1

        self._data_count += 1
        return True

    def is_exists(self, key):
        """
        :param key:
        :return:
        判断该值是否存在
        有任意一位为0 则肯定不存在
        """
        for time in range(self._hash_num):
            key_hashed_idx = mmh3.hash(key, self._hash_seed[time]) % self._bit_num
            if not self._bit_array[key_hashed_idx]:
                return False
        return True

    def copy(self):
        """
        :return: 返回一个完全相同的布隆过滤器实例
        复制一份布隆过滤器的实例
        """
        new_filter = BloomFilter(self.data_size, self.error_rate)
        return self._copy_param(new_filter)

    def _copy_param(self, filter):
        filter._bit_array = copy.deepcopy(self._bit_array)
        filter._bit_num = self._bit_num
        filter._hash_num = self._hash_num
        filter._hash_seed = copy.deepcopy(self._hash_seed)
        filter._data_count = self._data_count
        return filter

    def _is_half_fill(self):
        """
        判断数据是否已经超过容量的一半
        """
        return self._data_count > (self._hash_num // 2)

    def _adjust_param(self, data_size, error_rate):
        """
        :param data_size:
        :param error_rate:
        :return:
        通过数据量和期望的误报率 计算出 位数组大小 和 哈希函数的数量
        k为哈希函数个数    m为位数组大小
        n为数据量          p为误报率
        m = - (nlnp)/(ln2)^2
        k = (m/n) ln2
        """
        p = error_rate
        n = data_size
        m = - (n * (math.log(p, math.e)) / (math.log(2, math.e))**2)
        k = m / n * math.log(2, math.e)

        return int(m), int(k)

    def __len__(self):
        """"
        返回现有数据容量
        """
        return self._data_count

    def __contains__(self, key):
        """
        用于实现 in 判断
        >>> bf = BloomFilter(data_size=100000, error_rate=0.001)
        >>> bf.add("test")
        True
        >>> "test" in bf
        True
        """
        return self.is_exists(key)


class RedisFilter(BloomFilter):

    def __init__(self, host='localhost', port=6379, db=0, redis_key='bloomfilter_', password='', username=''):
        """
        :param host:
        :param port:
        :param db:
        :param key:
        """
        self.server = redis.Redis(host=host, port=port, db=db, password=password, username=username)
        self.redis_key = redis_key

        # 已存数据量
        self._data_count = 0

    def start(self, data_size, error_rate=0.001):
        """
        :param data_size: 所需存放数据的数量
        :param error_rate:  可接受的误报率，默认0.001
        :return:
        启动函数，通过数据量、误报率 确定位数组长度、哈希函数个数、哈希种子等
        """
        if not data_size > 0:
            raise ValueError("Capacity must be > 0")
        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")

        self.data_size = data_size
        self.error_rate = error_rate

        bit_num, hash_num = super()._adjust_param(data_size, error_rate)
        self._bit_num = bit_num if bit_num < (1 << 32) else (1 << 32)
        self._hash_num = hash_num
        # redis字符串最长为512M
        self._block_num = 1 if bit_num < (1 << 32) else math.ceil(math.ceil(bit_num/8/1024/1024)/512)
        # 将哈希种子固定为 1 - hash_num （预留持久化过滤的可能）
        self._hash_seed = [i for i in range(1, hash_num+1)]

        return True

    def add(self, key):
        """
        :param key: 要添加的数据
        :return:
        >>> bf = BloomFilter(data_size=100000, error_rate=0.001)
        >>> bf.add("test")
        True
        """
        if self._is_half_fill():
            raise IndexError("The capacity is insufficient")

        keyname = self.redis_key + str(sum(map(ord, key)) % self._block_num)

        key_hashed_idx = []
        for time in range(self._hash_num):
            key_hashed_idx.append(mmh3.hash(keyname, self._hash_seed[time]) % self._bit_num)

        lock = acquire_lock_with_timeout(self.server, key)
        if lock:
            for idx in key_hashed_idx:
                self.server.setbit(keyname, idx, 1)

            self._data_count += 1
            release_lock(self.server, key, lock)
            return True
        else:
            return False

    def is_exists(self, key):
        """
        :param key:
        :return:
        判断该值是否存在
        有任意一位为0 则肯定不存在
        """
        keyname = self.redis_key + str(sum(map(ord, key)) % self._block_num)

        lock = acquire_lock_with_timeout(self.server, key)

        for time in range(self._hash_num):
            key_hashed_idx = mmh3.hash(keyname, self._hash_seed[time]) % self._bit_num
            if not int(self.server.getbit(keyname, key_hashed_idx)):    # 类型？
                release_lock(self.server, key, lock)
                return False

        release_lock(self.server, key, lock)
        return True


if __name__ == '__main__':

    bf = RedisFilter()
    bf.start(1000, 0.0001)
    # 仅测试输出，正常使用时透明
    print(bf._bit_num, bf._hash_num)
    print(bf._block_num)
    print(bf._bit_num)

    a = ['when', 'how', 'where', 'too', 'there', 'to', 'when']
    for i in a:
        print(bf.add(i))

    print('xixi in bf?: ', 'xixi' in bf)

    b = ['when', 'xixi', 'haha']
    for i in b:
        if bf.is_exists(i):
            print('%s exist' % i)
        else:
            print('%s not exist' % i)

    print('bf had load data: ', len(bf))