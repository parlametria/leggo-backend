from django.contrib import admin

# Register your models here.
from tweets.models import Perfil, Pressao, Tweet, Engajamento


admin.site.register(Perfil)
admin.site.register(Pressao)
admin.site.register(Tweet)
admin.site.register(Engajamento)
