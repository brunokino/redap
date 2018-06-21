# -*- coding: utf-8 -*-

from .loader import core_settings

LOG_FORMAT = '%(asctime)s [%(process)d] [%(levelname)s] %(message)s'
AUTH_TYPE = core_settings['auth_type']

# Cross-origin resource sharing configuration
CORS_HEADERS = ['Origin', 'Content-Type', 'Accept', 'Authorization']
CORS_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD']
CORS_RESOURCES = {
    r'/api/*': {
        'origins': '*',
        'supports_credentials': True
    }
}

SQLALCHEMY_DATABASE_URI = core_settings['database_uri']
SQLALCHEMY_TRACK_MODIFICATIONS = False

SWAGGER = {
    'title': 'Lapdance',
    'description': 'HTTP/LDAP Gateway',
    'contact': {
        'responsibleDeveloper': 'Robert Wikman',
        'email': 'rbw@vault13.org',
        'url': 'http://github.com/rbw0/lapdance',
    },
    'specs_route': '/api-docs',
    'basePath': '/',
    'version': '0.0.2',
    'swagger_ui': True,
    'uiversion': 2,
    'securityDefinitions': {
        'APIKeyHeader': {
            'type': 'apiKey',
            'name': 'x-api-key',
            'in': 'header'
        },
    }
}
