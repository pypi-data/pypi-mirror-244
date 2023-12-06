import unittest

import django
from django.conf import settings
from django.core.management import call_command

# Setup a mock Django project, with an in-memory database.
# We need the authentication application and contenttypes. Django will not run without
# contenttypes loaded and the auth provides our user models, which is required to run
# the pipeline code.
#
# Do not attempt to place any code or Django imports before the setup and migrations are
# done it will not work and you will get an ImproperlyConfigured exception.

settings.configure()
settings.INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes',]
settings.DATABASES = DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:',}}
django.setup()  # Fake normal Django setup procedure.

# Migrate database to provide a backend for the auth module.
call_command("migrate", interactive=False)

# End Django setup procedure, you can now return to regular testing.

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

from apereo.pipelines.groups import cn_to_group_name, superuser, add_user_to_groups

class LDAPTestCase(unittest.TestCase):
    def test_cn(self):
        cn = 'cn=ops,ou=groups,dc=wikimedia,dc=org'
        self.assertEqual('ops', cn_to_group_name(cn))


class PermissionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        settings.REMOTE_AUTH_SUPERUSER_GROUPS = ['Mystery Inc.']
        return super().setUp()

    def tearDown(self) -> None:
        User.objects.all().delete()
        Group.objects.all().delete()
        return super().tearDown()

    def test_superuser(self):
        # Verify that user isn't already a superuser
        user = User.objects.create(username='shaggy', first_name='Norville', last_name='Rogers')
        user = superuser(user)
        self.assertFalse(user.is_superuser)

        # Add user to superuser group
        group = Group.objects.create(name='Mystery Inc.')
        user.groups.add(group)

        # Reload user to ensure that group membership has been persisted
        user = User.objects.get(username='shaggy')
        self.assertTrue(user.groups.filter(name='Mystery Inc.').exists())

        # Upgrade user to superuser
        user = superuser(user)
        self.assertTrue(user.is_superuser)


class PipelineBasicTestCase(unittest.TestCase):
    def setUp(self) -> None:
        settings.REMOTE_AUTH_SUPERUSER_GROUPS = ['Mystery Inc.']
        settings.REMOTE_AUTH_STAFF_GROUPS = ['labs']
        return super().setUp()

    def test_pipeline(self):
        # Test that all groups are created and assigned correctly.
        user = User.objects.create(username='vdinkley', first_name='Velma', last_name='Dinkley')
        data = {
            'response': {
                'name': 'Velma Dinkley',
                'memberOf': [
                    'cn=Mystery Inc.,ou=groups,dc=example,dc=org',
                    'cn=Drivers,ou=groups,dc=example,dc=org',
                    'cn=labs,ou=groups,dc=example,dc=org',
                ],
                'preferred_username': 'vdinkley',
                'email': 'vdinkley@example.org'
            }
        }

        add_user_to_groups(None, {}, 'OIDC', user, {}, **data)
        user = User.objects.get(username='vdinkley')
        self.assertEqual(len(Group.objects.all()), len(data['response']['memberOf']))
        self.assertCountEqual(Group.objects.all(), user.groups.all())

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

class PipelineLimitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        settings.REMOTE_AUTH_SUPERUSER_GROUPS = ['Mystery Inc.']
        settings.REMOTE_AUTH_STAFF_GROUPS = ['labs']
        settings.SOCIAL_AUTH_ALLOW_GROUPS = ['Mystery Inc.', 'labs']
        return super().setUp()

    def test_pipeline_limits(self):
        # Test that we do only create groups in the allow list.
        user = User.objects.create(username='fjones', first_name='Fred', last_name='Jones')
        data = {
            'response': {
                'name': 'Fred Jones',
                'memberOf': [
                    'cn=Mystery Inc.,ou=groups,dc=example,dc=org',
                    'cn=Drivers,ou=groups,dc=example,dc=org',
                    'cn=Detectives,ou=groups,dc=example,dc=org',
                ],
                'preferred_username': 'fjones',
                'email': 'fjones@example.org'
            }
        }

        add_user_to_groups(None, {}, 'OIDC', user, {}, **data)
        user = User.objects.get(username='fjones')
        self.assertFalse(Group.objects.filter(name='detectives'))
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_pipeline_group_removal(self):
        user = User.objects.create(username='dblake', first_name='Daphne', last_name='Blake')
        group = Group.objects.create(name='DYI')
        user.groups.add(group)

        data = {
            'response': {
                'name': 'Daphne Blake',
                'memberOf': [
                    'cn=Mystery Inc.,ou=groups,dc=example,dc=org',
                    'cn=Detectives,ou=groups,dc=example,dc=org',
                ],
                'preferred_username': 'dblake',
                'email': 'dblake@example.org'
            }
        }

        add_user_to_groups(None, {}, 'OIDC', user, {}, **data)
        user = User.objects.get(username='dblake')
        self.assertFalse(user.groups.filter(name='detectives'))
        self.assertFalse(user.groups.filter(name='DYI'))
        self.assertTrue(user.groups.filter(name='Mystery Inc.'))

    def test_pipeline_staff_permission_removal(self):
        # Test that is_staff and is_superuser is correctly removed, if the user
        # is not in the correct groups.
        user = User.objects.create(username='scooby', first_name='Scoobert', last_name='Doo')
        group, created = Group.objects.get_or_create(name='labs')
        user.groups.add(group)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        data = {
            'response': {
                'name': 'Scoobert Doo',
                'memberOf': [
                    'cn=bowling team,ou=groups,dc=example,dc=org',
                    'cn=snacks,ou=groups,dc=example,dc=org',
                ],
                'preferred_username': 'scooby',
                'email': 'scooby@example.org'
            }
        }

        add_user_to_groups(None, {}, 'OIDC', user, {}, **data)
        user = User.objects.get(username='scooby')
        self.assertFalse(user.groups.all())
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)