from django.db import models


class InfoGerais(models.Model):

    name = models.TextField()
    value = models.JSONField()
