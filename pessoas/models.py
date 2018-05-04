import json
from django.conf import settings
from django.db import models


def upload_image_pessoa(instance, filename):
    return 'pessoa/{user}/{filename}'.format(
        user=instance.user, filename=filename)


class PessoaQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('id', 'first_name', 'last_name'))
        return json.dumps(list_values)


class PessoaManager(models.Manager):
    def get_queryset(self):
        return PessoaQuerySet(self.model, using=self._db)


class Pessoa(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    picture = models.ImageField(
        upload_to=upload_image_pessoa, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = PessoaManager()

    def __str__(self):
        return self.first_name

    def serialize(self):
        try:
            picture = self.picture.url
        except:
            picture = ""
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'picture': picture
        }
        data = json.dumps(data)
        return data
