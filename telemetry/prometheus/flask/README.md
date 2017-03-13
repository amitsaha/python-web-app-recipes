## Recipe Index

[app1.py](app1.py) - Basic integration of Prometheus Python client to export a metrics endpoint
[app2.py](app1.py) - Export Statsd Metrics via Datadog to Prometheus Statsd bridge

Run it via: `` docker run -p 9102:9102 -p 9125:9125/udp          prom/statsd-exporter ``

To run multiple instances via `uwsgi`:

```
uwsgi --http :5000  --manage-script-name --mount /yourapplication=app1:app --enable-threads --processes 5
```

We will use the "test_app" label to aggregate the metrics
