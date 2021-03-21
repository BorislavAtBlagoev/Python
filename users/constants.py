import os

ADMIN_ROLE = 'Admin'
BARTENDER_ROLE = 'Bartender'
WAITER_ROLE = 'Waiter'

AUTH0_PREDEFINED_ROLES = [
    {
        "id": "rol_TVqbOH6eQ2uoSDWU",
        "name": "Admin",
        "description": "Admin"
    },
    {
        "id": "rol_cIes0MKgHmJ7E1gp",
        "name": "Bartender",
        "description": "Bartender"
    },
    {
        "id": "rol_cKsa4Sm4zg5hBZIU",
        "name": "Waiter",
        "description": "Waiter"
    }
]

AUTH0_URLS = {
    'issue_a_token': 'https://mm-restaurant-devcamp-2021-1.eu.auth0.com/' + 'oauth/token',
    'create_user': 'https://mm-restaurant-devcamp-2021-1.eu.auth0.com/' + 'api/v2/users',
    'assign_role': 'https://mm-restaurant-devcamp-2021-1.eu.auth0.com/' + 'api/v2/roles/{userRoleId}/users',
    'login_user': 'https://mm-restaurant-devcamp-2021-1.eu.auth0.com/' + 'authorize'
}

CLAIMS = {
    'roles': 'http://schemas.microsoft.com/ws/2008/06/identity/claims/role',
    'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
    'name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
}
