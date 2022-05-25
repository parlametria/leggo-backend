from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    empresa = models.CharField(max_length=200, default=None, blank=True, null=True)

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )

    def __str__(self):
        return self.usuario.email if self.usuario else "NO USER"


class UsuarioProposicao(models.Model):
    proposicao = models.CharField(max_length=100)

    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.proposicao
