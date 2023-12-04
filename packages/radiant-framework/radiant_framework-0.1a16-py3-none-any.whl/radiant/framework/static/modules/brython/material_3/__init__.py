"""
============
Material-Web
============

"""
from browser import html
from functools import cache

maketag = cache(html.maketag)


def __getattr__(attr):
    """"""
    def element(*args, **kwargs):

        if attr.startswith('_'):
            tag = maketag(f'{attr[1:].replace("_", "-")}')
        else:
            tag = maketag(f'md-{attr.replace("_", "-")}')

        kwargs = {k.rstrip('_'): v for k, v in kwargs.items()}
        return tag(*args, **kwargs)
    return element

