from django.contrib import admin
from .models import UsuarioProposicao
from api.model.proposicao import Proposicao

admin.site.register(UsuarioProposicao)
admin.site.register(Proposicao)

# Register your models here.
