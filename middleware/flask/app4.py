# This is an example of implementing middleware via
# decorators that Flask framework exposes namely:
#
# app.before_first_request
# app.before_request
# app.after_request
# There are blueprint specific decorators as well, such as:
# http://flask.pocoo.org/docs/0.12/api/#flask.Blueprint.before_request
# which are useful when you want to execute code which is blueprint
# specific rather than app specific

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


# Functions registered with before_request()
# are called in order they are registered
@app.before_request
def before_request1():
    # We can access the request object to access
    # any relevant information from the request
    app.logger.debug(request.headers)
    app.logger.info('before_request1 called')


@app.before_request
def before_request2():
    app.logger.info('before_request2 called')


# Functions registered with after_request get called
# in a "LIFO" order i.e. the function registered last
# gets called first and vice-versa
@app.after_request
def after_request1(resp):
    app.logger.info('after_request1 called')
    return resp


@app.after_request
def after_request2(resp):
    app.logger.info('after_request2 called')
    return resp


@app.errorhandler(500)
def handle_500(error):
    print("500 error handler called")
    app.logger.error(error)
    return str(error), 500


@app.route('/test')
def test():
    try:
        1/0
    except Exception:
        raise
    return 'test successful'

if __name__ == '__main__':
    app.run()
