"""Opt-in child-process diagnostics; outer controller enforces total timeout."""
import faulthandler


def bounded_timeout(value):
    if isinstance(value, tuple):
        return tuple(min(item, cap) if item is not None else cap
                     for item, cap in zip(value, (10, 25)))
    return (10, 25) if value is None else min(value, 25)


def main():
    import requests
    from colab_cli.cli import main as colab_main
    original = requests.sessions.Session.request

    def bounded_request(self, method, url, **kwargs):
        kwargs['timeout'] = bounded_timeout(kwargs.get('timeout'))
        return original(self, method, url, **kwargs)

    faulthandler.enable()
    faulthandler.dump_traceback_later(35, repeat=False)
    requests.sessions.Session.request = bounded_request
    try:
        colab_main()
    finally:
        requests.sessions.Session.request = original
        faulthandler.cancel_dump_traceback_later()


if __name__ == '__main__':
    main()
