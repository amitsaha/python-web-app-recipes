# This is an example of implementing middleware without
# using decorators
# Derived from http://steinn.org/post/flask-statsd
from flask import Flask, request
import logging


app = Flask(__name__)


# From https://github.com/benoitc/gunicorn/issues/379
# This gets called only *once* before first request to the
# app
@app.before_first_request
def setup_logging():
    # Configure app.logger to log to stderr
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


class MyMiddleware:

    def __init__(self, app):
        self.app = app
        self.wsgi_app = app.wsgi_app

    def __call__(self, environ, start_response):
        def start_response_wrapper(*args, **kwargs):
            self.app.logger.info('Request %s', request.headers)
            status = args[0].split(' ')[0]
            self.status = status
            return start_response(*args, **kwargs)

        self.app.logger.info('Calling the actual function')
        response = self.wsgi_app(environ, start_response_wrapper)
        self.app.logger.info(response)
        self.app.logger.info('I have a response now')
        return response

app.wsgi_app = MyMiddleware(app)


@app.route('/test')
def testing():
    return 'Testing'

if __name__ == '__main__':
    app.run(debug=True)
