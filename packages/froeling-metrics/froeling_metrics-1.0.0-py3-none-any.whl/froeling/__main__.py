import getpass
from .metrics import scrapmetrics
from .token import Token

import logging
logging.basicConfig()
logging.getLogger("urllib3").setLevel(logging.DEBUG)

login = input("Fröling user login: ")
password = getpass.getpass(prompt="Fröling user password: ")

try:
    token = Token(login, password, storage='token.txt')
    metrics = scrapmetrics(token=token, language='fr')
except Exception as error:
    print(error)
else:
    print()
    for facility, metrics in metrics.items():
        print(f"{facility=}")
        for metric in metrics:
            try:
                if 'stringListKeyValues' in metric:
                    value = metric['stringListKeyValues'][metric['value']]
                else:
                    value = metric['value'] + metric['unit']
            except Exception:
                value = metric.get('value')
            print(f" - {metric['name']}/{metric.get('displayName')}: {value}")

            
