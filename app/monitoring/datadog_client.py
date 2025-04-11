import os
from datadog import initialize, api, statsd


def setup_datadog():
    options = {
        "api_key": os.getenv("DD_API_KEY"),
        "app_key": os.getenv("DD_APP_KEY"),
    }
    initialize(**options)

def send_event(title, text, tags=None):
    setup_datadog()
    api.Event.create(title=title, text=text, tags=tags or [])

def send_metric(name, value=1, tags=None):
    statsd.increment(name, tags=tags or [])
