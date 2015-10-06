import requests
import urlparse

from functools import wraps
from minion.frontend.utils import frontend_config

# Decorator to add X-Minion-Backend-Key to the headers variable (or create it if not there); it also prepends
# the backend's URL to the (relative) path requested.  It only does this for relative URLs: for absolute URLs, it
# should act exactly like requests
def api_request(fn):
    @wraps(fn)
    def wrapper(url, **kwargs):
        # If the URL is a path, treat it like we're requesting a resource from the Minion backend
        if not urlparse.urlparse(url).netloc:
            # Pull out the config
            config = frontend_config().get('api', {})
            baseurl = config.get('url', '')
            key = config.get('key', 'SECRETKEYHERE')  # Invalid key, should be rejected by backend

            #  Fix the config URL, in case it was erroneously ended with /
            if baseurl[-1] == '/':
                baseurl = baseurl[:-1]

            url = baseurl + url

            # Add Minion API key to the request headers
            if 'headers' in kwargs:
                headers = kwargs.pop('headers')
            else:
                headers = {}
            headers['X-Minion-Backend-Key'] = key

            return fn(url, headers=headers, **kwargs)
        else:
            return fn(url, **kwargs)

    return wrapper

@api_request
def delete(url, **kwargs):
    return requests.delete(url, **kwargs)

@api_request
def get(url, **kwargs):
    return requests.get(url, **kwargs)

@api_request
def head(url, **kwargs):
    return requests.head(url, **kwargs)

@api_request
def options(url, **kwargs):
    return requests.options(url, **kwargs)

@api_request
def patch(url, **kwargs):
    return requests.patch(url, **kwargs)

@api_request
def post(url, **kwargs):
    return requests.post(url, **kwargs)

@api_request
def put(url, **kwargs):
    return requests.put(url, **kwargs)