#!/usr/bin/env python3
import os
import urllib
from app import create_app
from flask import url_for
from flask_script import Manager, Server

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

server = Server(host="0.0.0.0", port=5010)
manager.add_command("runserver", server)


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
