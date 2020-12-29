from .base_settings import *
import os

INSTALLED_APPS += [
    'rttl_admin.apps.RTTLAdminConfig',
]

if os.getenv('ENV') == 'localdev':
    DEBUG = True
    RTTL_ADMIN_GROUP = 'u_test_group'
    RESTCLIENTS_DAO_CACHE_CLASS = None
else:
    RTTL_ADMIN_GROUP = os.getenv('ADMIN_GROUP', '')
    RESTCLIENTS_DAO_CACHE_CLASS = 'rttl_admin.cache.Client'

SUPPORTTOOLS_PARENT_APP = 'RTTL.UW'
SUPPORTTOOLS_PARENT_APP_URL = '/'
