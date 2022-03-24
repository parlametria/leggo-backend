from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UsuarioProposicao(models.Model):
    proposicao = models.CharField(max_length=100)

    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.proposicao
