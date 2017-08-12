from __future__ import unicode_literals

from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


# HELPER FIELDS AND TABLES

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None,
                 max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


# CUSTOM USER CLASS AND MANAGER

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    ETHNICITY_CHOICES = (
        ('AS', 'Asian'),
        ('BL', 'Black'),
        ('LA', 'Latino'),
        ('ME', 'Middle Eastern'),
        ('MI', 'Mixed'),
        ('NA', 'Native American'),
        ('WH', 'White'),
        ('SA', 'South Asian'),
        ('OT', 'Other')
    )

    BODY_TYPE_CHOICES = (
        ('TO', 'Toned'),
        ('AV', 'Average'),
        ('LA', 'Large'),
        ('MU', 'Muscular'),
        ('SL', 'Slim'),
        ('ST', 'Stocky')
    )

    POSITION_CHOICES = (
        ('TO', 'Top'),
        ('VT', 'Vers Top'),
        ('VS', 'Versatile'),
        ('VB', 'Vers Bottom'),
        ('BO', 'Bottom')
    )

    REL_STATUS_CHOICES = (
        ('CO', 'Committed'),
        ('DA', 'Dating'),
        ('EN', 'Engaged'),
        ('EX', 'Exclusive'),
        ('MA', 'Married'),
        ('OR', 'Open Relationship'),
        ('PA', 'Partnered'),
        ('SI', 'Single')
    )

    HIV_STATUS_CHOICES = (
        ('NE', 'Negative'),
        ('NP', 'Negative, on PrEP'),
        ('PO', 'Positive'),
        ('PU', 'Positive, Undetectable')
    )

    email = models.EmailField(_('Email Address'), unique=True)
    display_name = models.CharField(_('Display Name'), max_length=50)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  TODO
    # language = models.ForeignKey(Language, default=1)
    about_me = models.CharField(max_length=255, null=True, blank=True)
    age = IntegerRangeField(min_value=18, max_value=100, null=True, blank=True)
    height = IntegerRangeField(min_value=122, max_value=241,
                               null=True, blank=True)
    weight = IntegerRangeField(min_value=41, max_value=272,
                               null=True, blank=True)
    ethnicity = models.CharField(
        max_length=2, choices=ETHNICITY_CHOICES, null=True, blank=True,
        verbose_name='Ethnicity'
    )
    body_type = models.CharField(
        max_length=2, choices=BODY_TYPE_CHOICES, null=True, blank=True,
        verbose_name='Body Type'
    )
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, null=True, blank=True,
        verbose_name='Position'
    )
    rel_status = models.CharField(
        max_length=2, choices=REL_STATUS_CHOICES, null=True, blank=True,
        verbose_name='Relationship Status'
    )
    hiv_status = models.CharField(
        max_length=2, choices=HIV_STATUS_CHOICES, null=True, blank=True,
        verbose_name='HIV Status'
    )
    hiv_test_date = models.DateField(null=True, blank=True,
                                     verbose_name='HIV Test Date')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name', ]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.email

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.display_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
