import ssl
import urllib3

from requests.adapters import HTTPAdapter



class Ssl3Adapter(HTTPAdapter):
    def __init__(self, num_pools=500,maxsize=2000):
        retry = urllib3.Retry(connect=3, backoff_factor=0.5)
        self.poolmanager = urllib3.PoolManager(num_pools=num_pools, maxsize=maxsize,retries=retry, ssl_version=ssl.PROTOCOL_SSLv3)
        self.disable_warnings = urllib3.disable_warnings()
