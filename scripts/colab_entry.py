"""Process-local CLI diagnostics and HTTP timeout bound; no credential logging."""
import faulthandler
import requests

faulthandler.enable()
faulthandler.dump_traceback_later(35, repeat=False)
original_request = requests.sessions.Session.request


def bounded_request(self, method, url, **kwargs):
    timeout = kwargs.get('timeout')
    if timeout is None:
        kwargs['timeout'] = (10, 25)
    elif isinstance(timeout, (float, int)):
        kwargs['timeout'] = min(timeout, 25)
    return original_request(self, method, url, **kwargs)


requests.sessions.Session.request = bounded_request
from colab_cli.cli import main
main()
