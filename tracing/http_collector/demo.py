from flask import Flask, request

app = Flask(__name__)


from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span

import requests
import time

def http_transport(encoded_span):
    # The collector expects a thrift-encoded list of spans. Instead of
    # decoding and re-encoding the already thrift-encoded message, we can just
    # add header bytes that specify that what follows is a list of length 1.
    body = '\x0c\x00\x00\x00\x01' + encoded_span
    requests.post(
        'http://localhost:9411/api/v1/spans',
        data=body,
        headers={'Content-Type': 'application/x-thrift'},
    )

@zipkin_span(service_name='webapp', span_name='do_stuff')
def do_stuff():
    time.sleep(5)
    headers = create_http_headers_for_new_span()
    requests.get('http://localhost:6000/service1/', headers=headers)
    return 'OK'

@app.route('/')
def index():
    with zipkin_span(
        service_name='webapp',
        span_name='index',
        transport_handler=http_transport,
        port=5000,
        sample_rate=100, #0.05, # Value between 0.0 and 100.0
    ):
        do_stuff()
        time.sleep(10)
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)

