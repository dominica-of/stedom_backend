from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)
    specification = models.CharField(_('specification'), max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['-email']
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.id])

    def get_email(self):
        return '%s' % self.email

    def __str__(self):
        return '%s' % self.full_name
