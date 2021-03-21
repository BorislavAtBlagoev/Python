import json
import os

import requests

from users.constants import AUTH0_PREDEFINED_ROLES, AUTH0_URLS


class Auth0Helper:
    token = None

    @staticmethod
    def _get_role_id(role):
        for data in AUTH0_PREDEFINED_ROLES:
            if role == data['name']:
                return data['id']

    def _set_token(self):
        data = {
            "client_id": 'yPumHwHTMQunpFK7nDNueOuO00TBVSie',
            "client_secret": 'H5BbcB96ciz5Vn_PCyEOusRFoeDClBKK-mGcToxz62fZQ6eK45YaftMB3MI3uBZL',
            "audience": 'https://mm-restaurant-devcamp-2021-1.eu.auth0.com/api/v2/',
            "grant_type": 'client_credentials'
        }

        response = requests.post(AUTH0_URLS['issue_a_token'], data)
        result = json.loads(response.text)

        self.token = result['access_token']

    def _create_user(self, email, name, password):
        data = {
            "email": email,
            "user_metadata": {},
            "app_metadata": {},
            "name": name,
            "password": password,
            "connection": "Username-Password-Authentication"
        }

        headers = {"authorization": "Bearer {}".format(self.token)}
        response = requests.post(AUTH0_URLS['create_user'], data=data, headers=headers)
        result = json.loads(response.text)

        return result['user_id']

    def _assign_role(self, user_id, role):
        data = {
            "users": [
                user_id
            ]
        }

        headers = {"Authorization": "Bearer {}".format(self.token)}
        url = AUTH0_URLS['assign_role'].format(userRoleId=self._get_role_id(role))
        requests.post(url, json=data, headers=headers)

    def create_user(self, email, name, password, role):
        self._set_token()

        user_id = self._create_user(email, name, password)
        self._assign_role(user_id, role)

        return user_id

    def login_user(self, email, password):
        pass
