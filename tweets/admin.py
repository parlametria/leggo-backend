from django.contrib import admin

# Register your models here.
from tweets.models import ParlamentarPerfil, Pressao, Tweet, Engajamento


admin.site.register(ParlamentarPerfil)
admin.site.register(Pressao)
admin.site.register(Tweet)
admin.site.register(Engajamento)
