from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tweets.models import Tweet, TweetsInfo, ParlamentarPerfil


@receiver(post_save, sender=ParlamentarPerfil, dispatch_uid="get_parlamentares_info_ref")
def get_parlamentares_info(sender,  instance, created, **kwargs):
    tweet_info = TweetsInfo.processa_atual_info()

    if(created):
        if(tweet_info):
            tweet_info.numero_parlamentares_sem_perfil = tweet_info.numero_parlamentares_sem_perfil - 1
            tweet_info.save()
    else:
        return tweet_info


@receiver(post_delete, sender=ParlamentarPerfil, dispatch_uid="get_parlamentares_info_ref")
def del_tweets_parlamentares(sender,  instance, **kwargs):
    tweet_info = TweetsInfo.processa_atual_info()
    tweet_info.numero_parlamentares_sem_perfil = tweet_info.numero_parlamentares_sem_perfil + 1
    tweet_info.save()
