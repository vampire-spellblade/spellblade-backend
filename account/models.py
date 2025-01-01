# pylint: disable=missing-module-docstring

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    Group as DjangoGroup,
)
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractUser):
    '''
    User model tailored to use email instead of username,
    and enforce use of first and last name fields.
    '''
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

class Group(DjangoGroup):
    '''Proxy model for DjangoGroup'''

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        proxy = True

'''
A more complex User design to support multiple emails.

Have an Emails table. This table store a unique list of all known emails irrespective of user.

Then have the users table. The user table will use two foreign key. Firstly, it'll reference the Emails table
for the primary email. Secondly, it'll reference the third table which will be produced by ManyToManyField
which will associate a user to a list of emails.

Thus, a user will start with a single primary email and that can be changed by the user to any other email in
Non-User specific emails database.

To prevent the problem that comes out in the above, views will be responsible for validating the emails instead.
Unluckily, I've no idea how to do so at the database level.

Unluckily it also has other problems such as the fact that if a user account is deleted, the emails table will
remain untouched because it's not easy to determine if the user was the only account using an email or not.
Additionally, user_id and email_id must be unique together which is quite easy to achieve in django luckily.

The problem might not be a trouble sometimes but there's cases unluckily such as when emails are to be sent to all
active users in which case either emails can be just sent to everyone instead and it'll take less effort, or
complex queries are run to filter the users to only active ones and to only certain emails. In fact, emails become
another issue with this when we consider they have to be checked and such adds overhead, so not deleting them at once a week
is a feasible solution but adds complexity to scheduled tasks for keeping the database clean and might break GDPR for example.

# I've no idea what I'm trying to achieve so the above is a lot more rambling.
'''
