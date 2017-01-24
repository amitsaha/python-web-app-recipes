# Example from http://flask.pocoo.org/docs/0.11/patterns/deferredcallbacks/
from flask import Flask, request, g
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


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f


@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'after_request_callbacks', ()):
        response = func(response)
    return response


@app.route('/test')
def test():
    @after_this_request
    def callback1(response):
        app.logger.info('callback1 called')
        return response
    return 'rest'


if __name__ == '__main__':
    app.run(debug=True)
