# In complete
from flask import Flask
import flask

app = Flask(__name__)


@app.route('/')
def index():
    return flask.current_app.config['cfgfile']

if __name__ == '__main__':
    app.run(debug=True)
