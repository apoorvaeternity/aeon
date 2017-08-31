from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your models here.
class ProfileModelManager(models.Manager):
    def _create_auth_token(self, user):
        Token.objects.get_or_create(user=user)
        return user.auth_token.key

    def _delete_auth_token(self, user):
        return Token.objects.get(user=user).delete()


class Profile(models.Model):
    user = models.ForeignKey(User)
    avatar = models.ImageField()
    auth_token = models.CharField(max_length=255)
    objects = ProfileModelManager()

    def __str__(self):
        return self.user.username
