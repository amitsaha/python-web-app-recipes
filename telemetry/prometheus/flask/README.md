## Recipe Index

[app1.py](app1.py) - Basic integration of Prometheus Python client to export a metrics endpoint

To run multiple instances via `uwsgi`:

```
uwsgi --http :5000  --manage-script-name --mount /yourapplication=app1:app --enable-threads --processes 5
```

We will use the "test_app" label to aggregate the metrics
