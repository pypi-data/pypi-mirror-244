# Apereo CAS pipeline for Django Social Auth

When using SSO with Netbox is it not normally possible to have groups syncronized.
This pipeline for Django Social Auth takes the data in the OIDC response from
Apereo CAS and extracts the "memberOf" field and adds the user to those groups,
creating any missing groups in the process.

It is also possible to configure certain groups to grant staff and superuser
permessions to a user, based on group membership.

# Usage

Add the pipeline to the SOCIAL_AUTH_PIPELINE variable, e.g. if you using the standard
pipelines, if in doubt, then you most likely are, simply add the following to you
Netbox config:

```
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'netbox.authentication.user_default_groups_handler',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'apereo.pipelines.groups.add_user_to_groups',
)
```

With "apereo.pipeline.groups.add_user_to_groups" being the module path to the actual pipeline.


# Configuration

In some cases it's not required or even desirable to syncronize all groups returned by
Apereo CAS. You can limit the group you want by setting SOCIAL_AUTH_ALLOW_GROUPS. See example
below. This will ensure that only the listed groups are created and associated to users.

```
SOCIAL_AUTH_ALLOW_GROUPS = ['ops', 'staff']
```

The pipeline can automatically assign staff and superuser priviledges if configured.
Set the two standard Netbox configuration variables:

* REMOTE_AUTH_SUPERUSER_GROUPS
* REMOTE_AUTH_STAFF_GROUPS

These can be a string or an array of string.

```
REMOTE_AUTH_SUPERUSER_GROUPS = ['ops', 'wmf']
REMOTE_AUTH_STAFF_GROUPS = 'wmf'
```

If a user is a member of the listed groups the pipeline will ensure that the user attributes
"is_superuser" and "is_staff" is set to True.
