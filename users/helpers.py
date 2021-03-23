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
            "client_id": os.environ.get('AUTH0_CLIENT_ID'),
            "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
            "audience": os.environ.get('AUTH0_AUDIENCE'),
            "grant_type": os.environ.get('AUTH0_GRAND_TYPE')
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
