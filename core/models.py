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
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True)
    objects = ProfileModelManager()

    def __str__(self):
        return self.user.username


class Objective(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField()
    target_time=models.TimeField()

    def __str__(self):
        return self.title


class Milestone(models.Model):
    objective = models.ForeignKey(Objective)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField()
    target_time = models.TimeField()

    def __str__(self):
        return self.title
