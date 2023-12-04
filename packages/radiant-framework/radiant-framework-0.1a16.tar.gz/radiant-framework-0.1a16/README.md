# Radiant Framework

A Brython Framework for Web Apps development.

![GitHub top language](https://img.shields.io/github/languages/top/un-gcpds/brython-radiant?)
![PyPI - License](https://img.shields.io/pypi/l/radiant?)
![PyPI](https://img.shields.io/pypi/v/radiant?)
![PyPI - Status](https://img.shields.io/pypi/status/radiant?)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/radiant?)
![GitHub last commit](https://img.shields.io/github/last-commit/un-gcpds/brython-radiant?)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/UN-GCPDS/brython-radiant?)
[![Documentation Status](https://readthedocs.org/projects/radiant/badge/?version=latest)](https://radiant-framework.readthedocs.io/en/latest/?badge=latest)

Radiant is a web framework that is built on top of [Brython](https://brython.info/), which is an implementation of *Python* in the browser. This means that you can write your web applications using *Python* syntax, rather than having to deal with HTML, CSS, or JavaScript. 

Radiant allows you to write your application code once, and have it run both in the browser and on the server. When running on the server, Radiant uses the [Tornado](https://www.tornadoweb.org/) web server to serve up your application. It also sets up the local path for serving static files, which means that you can include images, stylesheets, and other assets in your application. 

When your application is run in the browser, Radiant uses Brython to execute your *Python* code. This allows you to write your code once, and have it run seamlessly in both environments. Radiant also provides a custom HTML template that is configured at runtime to import the same script that you wrote for the server-side code. 

Overall, Radiant is a powerful tool for developers who want to build web applications using *Python*. It allows you to write your code once, and have it run both on the server and in the browser. This can help streamline your development process, and allow you to focus on writing high-quality code, rather than worrying about the details of web development.

## Installation

To install Radiant, you can use ```pip```, the Python package manager:


```python
pip install radiant
```

## Bare minimum

To help you get started with Radiant, let's walk through a bare minimum example. This example will show you how to create a simple web page that displays some text. We'll use the Radiant framework to create the page and run it on a local server. This is a great way to get a feel for how Radiant works, and to start exploring its features.

To follow along with this example, you'll need to have Radiant installed on your system. If you haven't done this yet, please see the [Installation](#installation) section for instructions on how to install Radiant. Once you have Radiant installed, you're ready to go!


```python
from radiant.framework.server import RadiantAPI
from browser import document, html


class BareMinimum(RadiantAPI):

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        document.select_one('body') <= html.H1('Radiant-Framework')


if __name__ == '__main__':
    BareMinimum()
```


```python

```
