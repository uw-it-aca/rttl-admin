from memcached_clients import RestclientPymemcacheClient


class Client(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        return 60 * 60
