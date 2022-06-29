from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tweets.models import Tweet, TweetsInfo, ParlamentarPerfil
from api.model.entidade import Entidade
from api.views.entidade_serializer import ParlamentaresExercicioList
from types import SimpleNamespace
from datetime import datetime


def recupera_parlmanetares_casa(casa):
    request = {
        "query_params": {
            "casa": f"{casa}"
        }
    }

    _request = SimpleNamespace(**request)

    parlas = ParlamentaresExercicioList()
    parlas.request = _request
    parlas.get_queryset()
    return parlas.parlamentares


def procura_parlamentares_sem_perfil():
    senadores = recupera_parlmanetares_casa('senado')
    deputados = recupera_parlmanetares_casa('camara')
    CORRIGIR_FALTA_SEN = 1

    # total_parlamentares = len(senadores) + len(deputados) + CORRIGIR_FALTA_SEN

    def calcula_falta_por_casa(casa):
        nao_encontrado = 0
        for parlamentar in casa:
            try:
                ent = Entidade.objects.get(id=parlamentar.id)
                pp = ParlamentarPerfil.objects.get(entidade=ent)
            except (Entidade.DoesNotExist, ParlamentarPerfil.DoesNotExist):
                nao_encontrado = nao_encontrado + 1
        return nao_encontrado

    senado_nao_encontrado = calcula_falta_por_casa(senadores) + CORRIGIR_FALTA_SEN
    camara_nao_econtrado = calcula_falta_por_casa(deputados)

    sem_perfil_total = (senado_nao_encontrado + camara_nao_econtrado)

    return sem_perfil_total, senado_nao_encontrado, camara_nao_econtrado


@receiver(post_save, sender=Tweet, dispatch_uid="get_tweets_info_ref")
def get_tweets_info(sender,  instance, created, **kwargs):
    tweet_info = TweetsInfo.processa_atual_info()
    if(created):
        if(tweet_info):
            novo_tweet_info = TweetsInfo(
                tweet_mais_antigo=tweet_info.tweet_mais_antigo,
                tweet_mais_novo=instance,
                numero_parlamentares_sem_perfil=tweet_info.numero_parlamentares_sem_perfil,
                numero_total_tweets=tweet_info.numero_total_tweets+1
            )
            novo_tweet_info.save()
            return novo_tweet_info
        else:
            tweets = Tweet.objects.all()
            primeiro_tweet_info = TweetsInfo(
                tweet_mais_antigo=tweets.first(),
                tweet_mais_novo=tweets.reverse().first(),
                numero_total_tweets=tweets.count(),
                numero_parlamentares_sem_perfil=procura_parlamentares_sem_perfil()[
                    0],
            )
            primeiro_tweet_info.save()
            return primeiro_tweet_info
    else:
        return tweet_info


@receiver(post_delete, sender=Tweet, dispatch_uid="get_tweets_info_ref")
def del_tweets(sender,  instance, **kwargs):
    tweets_info = TweetsInfo().processa_atual_info()
    novo_tweets_info = TweetsInfo()
    tweets = Tweet.objects.all()
    novo_tweets_info.tweet_mais_novo = tweets.reverse().first()
    novo_tweets_info.tweet_mais_antigo = tweets.first()
    novo_tweets_info.numero_total_tweets = tweets_info.numero_total_tweets - 1
    novo_tweets_info.numero_parlamentares_sem_perfil = tweets_info.numero_parlamentares_sem_perfil
    novo_tweets_info.save()
