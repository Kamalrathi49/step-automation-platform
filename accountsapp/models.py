from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class GuideeProflie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guidee_user')
    invited_by = models.ManyToManyField(User, blank=True, related_name='invited_by' )

    def __str__(self):
        return self.user.username
