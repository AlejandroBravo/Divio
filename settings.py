# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-django-cms',
    'aldryn-bootstrap3',
    'aldryn-newsblog',
    'djangocms-googlemap',
    'djangocms-history',
    'djangocms-snippet',
    'djangocms-style',
    'djangocms-text-ckeditor',
    'djangocms-video',
    'django-filer',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTHENTICATION_BACKENDS = (
'django_auth_ldap.backend.LDAPBackend',
'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = 'ldap://192.168.2.206'

AUTH_LDAP_BIND_DN = "cn=admin,dc=planetexpress,dc=com"
AUTH_LDAP_BIND_PASSWORD = "GoodNewsEveryone"
useldapgroups = True

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'ou=people,dc=planetexpress,dc=com',
    ldap.SCOPE_SUBTREE,
    '(uid=%(user)s)',
)

AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'ou=people,dc=planetexpress,dc=com',
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfNames)',
)

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'cn',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_CONNECTION_OPTIONS = {
ldap.OPT_REFERRALS: 0
}

# all django settings can be altered here

INSTALLED_APPS.extend([
    # add your project specific apps here
     'django_extensions',
     'creasitios',
])

