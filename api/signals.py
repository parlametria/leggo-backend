from django.db.models.signals import post_save
from django.dispatch import receiver
from unittest import skip
from api.model.proposicao import Proposicao
from usuario.models import UsuarioProposicao


@receiver(post_save, sender=Proposicao, dispatch_uid="update_user_ref")
def update_user(sender, instance, **kwargs):
    encontrouProposicao = UsuarioProposicao.objects.filter(proposicao=instance.id_leggo)
    if not encontrouProposicao:
        up = UsuarioProposicao()
        up.proposicao = instance.id_leggo
        up.save()
        return up
    else:
        print(encontrouProposicao[0].usuarios.all())
        return encontrouProposicao[0].usuarios.all()
