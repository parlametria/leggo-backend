from django.contrib import admin

from .models import UsuarioProposicao, Perfil, VerfificacaoEmail
from api.model.proposicao import Proposicao

admin.site.register(UsuarioProposicao)
admin.site.register(Proposicao)
admin.site.register(Perfil)
admin.site.register(VerfificacaoEmail)
