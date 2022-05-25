from django.contrib import admin

from .models import UsuarioProposicao, Profile
from api.model.proposicao import Proposicao

admin.site.register(UsuarioProposicao)
admin.site.register(Proposicao)
admin.site.register(Profile)
