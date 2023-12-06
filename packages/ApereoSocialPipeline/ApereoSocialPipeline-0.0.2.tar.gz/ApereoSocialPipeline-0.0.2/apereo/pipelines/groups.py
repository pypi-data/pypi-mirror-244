# SPDX-License-Identifier: GPL-3.0-or-later
# Pipeline for Python Social Auth.
# Allow social_auth to create Django groups from the 
# data provided by the Apereo CAS OIDC callback.
#
# CAS will return groups in the "memberOf" field as
# LDAP CNs. We extra the group names and add the
# authenticated user to the relevant groups.
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Hook into django social auth logger
logger = logging.getLogger('social')


def cn_to_group_name(cn:str) -> str:
    # Get the CN of the group to use as name.
    # E.g. cn=ops,ou=groups,dc=wikimedia,dc=org becomes "ops"
    return cn.split(',')[0].lstrip('cn=')


def superuser(user):
    groups = getattr(settings, 'REMOTE_AUTH_SUPERUSER_GROUPS', [])
    if isinstance(groups, str):
        groups = [groups,]

    user.is_superuser = len(set(groups) & set(user.groups.all().values_list('name', flat=True))) > 0
    user.save()
    return user

def staff(user):
    groups = getattr(settings, 'REMOTE_AUTH_STAFF_GROUPS', [])
    if isinstance(groups, str):
        groups = [groups,]

    user.is_staff = len(set(groups) & set(user.groups.all().values_list('name', flat=True))) > 0
    user.save()
    return user

def add_user_to_groups(strategy, details, backend, user=None, *args, **kwargs) -> None:
    logger.debug(f'strategy: {strategy}, details: {details}, backend: {backend}, user: {user}, args: {args}, kwargs: {kwargs}')
    if not user:
        logger.warning('backend: %s, details: %s, user is None', backend, details)
        return

    # Convert the user object to a real Django User object.
    User = get_user_model()
    user = User.objects.get(username=user.username)
    groups = kwargs.get('response', {}).get('memberOf', [])

    oidc_groups = []
    # Add user to any new groups
    for group in groups:
        name = cn_to_group_name(group)

        if hasattr(settings, 'SOCIAL_AUTH_ALLOW_GROUPS') and name not in settings.SOCIAL_AUTH_ALLOW_GROUPS:
            continue

        g, created = Group.objects.get_or_create(name=name)
        oidc_groups.append(g)

        logger.info('backend: %s, group: %s, created: %s', backend, g.name, created)
        user.groups.add(g)

    # Remove unneeded groups
    for group in user.groups.all():
        if user.get_username() == 'dblake':
            print(oidc_groups)
        if group not in oidc_groups:
            user.groups.remove(group)

    superuser(user)
    staff(user)