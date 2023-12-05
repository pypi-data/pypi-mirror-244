# django-health-check-prometheus

This is a prometheus adapter for django health check, it will expose the health check results as prometheus metrics.

## Usage
```shell
pip install django-health-check-prometheus
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_health_check_prometheus',
    ...
]
```