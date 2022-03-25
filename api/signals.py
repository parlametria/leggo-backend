from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from api.model.proposicao import Proposicao
from usuario.models import UsuarioProposicao


@receiver(post_save, sender=Proposicao, dispatch_uid="update_user_ref")
def update_user(sender, instance, **kwargs):
    print("singal")
    encontrouProposicao = UsuarioProposicao.objects.filter(proposicao=instance.id_leggo)
    if not encontrouProposicao:
        print("Não encontrado!")
        up = UsuarioProposicao()
        up.proposicao = instance.id_leggo
        up.save()
    else:
        print("Usuários interessados")
        print(encontrouProposicao.usuarios)
