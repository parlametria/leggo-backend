from django.contrib.postgres.fields import JSONField
from django.db import models
class InfoGerais(models.Model):

    name = models.TextField()
    value = JSONField()