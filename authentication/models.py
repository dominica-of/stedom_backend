from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

LEARNER = 'learner'
INSTRUCTOR = 'instructor'

USER_TYPE_CHOICES = (
    (LEARNER, 'Learner'),
    (INSTRUCTOR, 'Instructor'),
)


class User(AbstractUser):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))

    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)
    specification = models.CharField(_('specification'), max_length=100)
    rating = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, blank=True, null=True)
    user_type = models.CharField(_('user type'), max_length=20, choices=USER_TYPE_CHOICES, default=LEARNER)

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


class Booking(models.Model):
    date_time = models.DateTimeField(blank=True, null=True)
    instructor = models.ForeignKey(User, related_name="instructor", on_delete=models.CASCADE)
    learner = models.ForeignKey(User, related_name="learner", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_time']
        verbose_name = _('booking')
        verbose_name_plural = _('Bookings')
