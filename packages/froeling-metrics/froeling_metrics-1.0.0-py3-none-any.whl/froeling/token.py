import base64
import datetime
import functools
import json
import os

import requests


class Token:
    RENEW_BEFORE_EXPIRY = datetime.timedelta(minutes=15)

    def __init__(self, login, password, storage=None):
        self._login = login
        self._password = password
        self._storage = storage
        self.expiry = datetime.datetime.now()
        self.subject = None
        self.issuer = None
        if self._storage:
            try:
                self.tokenstr = open(self._storage).read()
                self._decode()
            except:
                pass        
        self.renew()

    def __str__(self):
        return self.tokenstr

    def renew(self):
        tokenisvalid = True
        if self.subject != self._login:
            tokenisvalid = False
        if self.issuer != "froeling-connect-api":
            tokenisvalid = False
        if datetime.datetime.now() + Token.RENEW_BEFORE_EXPIRY > self.expiry:
            tokenisvalid = False
        if tokenisvalid:
            return

        payload = dict(osType='web', username=self._login, password=self._password)
        response = requests.post('https://connect-api.froeling.com/connect/v1.0/resources/login', json=payload)
        response.raise_for_status()
        self.tokenstr = response.headers['Authorization'].split()[1]
        self._decode()
        if self._storage:
            try:
                with open(self._storage, 'w', opener=functools.partial(os.open, mode=0o600)) as f:
                    f.write(self.tokenstr)
            except:
                pass

    def _decode(self):
        header, payload, signature = self.tokenstr.split('.')
        payload = json.loads(base64.b64decode(payload + '=='))
        self.userid = payload['userId']
        self.expiry = datetime.datetime.fromtimestamp(payload['exp'])
        self.subject = payload['sub']
        self.issuer = payload['iss']
