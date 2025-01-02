# pylint: disable=missing-module-docstring
from django.db import models
from django.contrib.auth.models import Group as DjangoGroup

class Group(DjangoGroup):
    '''Proxy model for DjangoGroup.'''

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        proxy = True

# TODO: Add a custom user model.
# Plan:
# 1. Update the username validator. By default, it uses the following code. Overwriting is feasible and actually quite easy.
# As part of the above step, username shouldn't allow using numbers at the start. They're fine anywhere else.
# Also the current regex allows usernames like _, @, etc. To this, I say @ will be removed. _ is supported through an unknown
# aspect of regex which is fine by me but using two special characters together shouldn't be possible. This includes __, _.,
# -_, etc.
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0
# 2. I've not decided properly on it yet if I want to make email field unique or not.
# Depending on this, I might have to also write a custom authenticate function or create a second authenticate function
# independent from first to allow logins with email. In the current app, it's feasible to work with two endpoints and not one
# for the sake of logging users in with either method. Admin portal will be untouched since I'll eventually remove it
# at a later date and I don't want to do the struggle of adding a way to login with either email or password.
# 3. I considered previously if it's feasible to store emails in a separate table. This primary considers that
# each user should have a primary email responsible for always receiving a particular set of notifications, and
# emails table is again associated to users table with a ManyToManyField for the purposes of defining backup emails.
# Note that primary email must also be a backup email in this design and the two are not mutually exclusive.
# 4. How to check OTPs? So this complex topic is already directly associated with using email for verification.
# The idea is basically that for example Hoyoverse allows users to login with either username or email, and
# When signing up, there's two forms. On first, user enters the emails and beside verification code field, there's a
# send OTP button. Once verified, user goes to next form where they enter username and password to complete the process.
# I suppose you can see how different this method is compared to what is expected to normal method in a lot of apps where
# account is created first and then verified which changes it from inactive to active.
