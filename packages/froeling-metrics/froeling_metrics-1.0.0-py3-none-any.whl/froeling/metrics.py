import base64
import json
import pathlib
import pprint

from .token import Token

import requests


def scrapmetrics(login=None, password=None, *, token=None, language=None):
    if (login or password) and token:
            raise ValueError("cannot give login/password and token")
    if not login and not password and not token:
            raise ValueError("missing login/password or token")
    if login or password:
        if not login or not password:
            raise ValueError("login and password should be both given")
        token = Token(login, password)

    # Ensure the token is not expired and prepare HTTP requests
    token.renew()
    userid = token.userid
    session = requests.Session()
    session.headers.update(dict(Authorization=f'Bearer {token}'))
    if language:
        session.headers.update({'Accept-Language': language})

    metrics = {}

    # List the facilities to which the token gives access
    facilityresponse = session.get(
        f'https://connect-api.froeling.com/connect/v1.0/resources/service/user/{userid}/facility')
    facilityresponse.raise_for_status()

    # For each facility, list the components
    for facility in (f['facilityId'] for f in facilityresponse.json()):
        componentlistresponse = session.get(
            f'https://connect-api.froeling.com/fcs/v1.0/resources/user/{userid}/facility/{facility}/componentList')
        componentlistresponse.raise_for_status()

        # For each component, iterate over the metrics
        for component in (c['componentId'] for c in componentlistresponse.json()):
            componentresponse = session.get(
                f'https://connect-api.froeling.com/fcs/v1.0/resources/user/{userid}/facility/{facility}/component/{component}')
            componentresponse.raise_for_status()
            for name, metric in itermetricsinobj(componentresponse.json()):
                # there are duplicated metrics (same name), keep the last one
                metrics.setdefault(facility, {})[name] = metric

    return {k: list(v.values()) for k, v in metrics.items()}


def itermetricsinobj(obj):
    # Recursively find metrics in obj
    # a metric is a dict with at least the two keys: id and name
    if isinstance(obj, dict):
        if 'id' in obj:
            if 'name' in obj:
                name = obj['name']
                yield name, obj
        else:
            for value in obj.values():
                yield from itermetricsinobj(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from itermetricsinobj(item)
