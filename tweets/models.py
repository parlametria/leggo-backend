from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


from api.model.entidade import Entidade
from api.model.etapa_proposicao import Proposicao
from api.model.interesse import Interesse
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from dotenv import dotenv_values
import tweepy
import json


class ParlamentarPerfil(models.Model):
    """
    O perfil pode ser tanto de um parlamentar, quanto de uma personalidade
    """
    entidade = models.OneToOneField(
        Entidade,
        related_name='entidadePerfil',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    is_personalidade = models.BooleanField()
    # if a person has more than one account?
    twitter_id = models.CharField(max_length=40, default=None, null=True)

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.twitter_id

    def populate_parlamentar(self):
        parlamentares = Entidade.objects.all()

        for parlamentar in parlamentares:
            perfil = ParlamentarPerfil(entidade=parlamentar, is_personalidade=False,)
            perfil.save()


class Tweet(models.Model):

    proposicao = models.ManyToManyField(Proposicao)
    # interesse = models.TextField()
    author = models.ForeignKey(ParlamentarPerfil, related_name="author",
                               on_delete=models.SET_NULL, null=True, blank=True)

    id_author = models.CharField(null=False, max_length=40, default=0)
    id_tweet = models.CharField(null=False, max_length=40, default=0)

    text = models.TextField()

    data_criado = models.DateField(null=False)

    likes = models.IntegerField(null=False)
    retweets = models.IntegerField(null=False)
    respostas = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.id_tweet}\n{self.text}'

    @classmethod
    def get_paginate(self, req, proposicao):
        counter = 0

        for page in req:
            for tweet in page.data:
                counter = counter + 1

                new_tweet = Tweet(
                    id_tweet=tweet.id,
                    id_author=tweet.author_id,
                    text=tweet.text,
                    data_criado=tweet.created_at,
                    likes=tweet.public_metrics.get('like_count'),
                    retweets=tweet.public_metrics.get('retweet_count'),
                    respostas=tweet.public_metrics.get('reply_count')

                )
                new_tweet.save()
                new_tweet.proposicao.add(proposicao)
                try:
                    perfil = ParlamentarPerfil.objects.get(twitter_id=tweet.author_id)
                    if(perfil):
                        new_tweet.author = perfil
                        new_tweet.save()
                except ParlamentarPerfil.DoesNotExist as e:
                    pass
                    # print(e)

    def get_recent(self, search, id_proposicao, end_time, start_time, order='relevancy', n_results=10):
        BEARER_TOKEN = dotenv_values(f"./.ENV").get('BEARER_TOKEN')
        client = tweepy.Client(BEARER_TOKEN)
        expansions = ['author_id']
        # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
        fields = ['created_at', 'public_metrics']

        proposicao = Proposicao.objects.get(id=id_proposicao)

        req = tweepy.Paginator(client.search_recent_tweets,
                               search,
                               end_time=end_time,
                               start_time=start_time,
                               max_results=n_results,
                               sort_order=order,
                               expansions=expansions,
                               tweet_fields=fields)

        self.get_paginate(req, proposicao)
        return req


class TweetsInfo(models.Model):
    """
    Criada a tabela com as informações de coletas de tweets
    Evita que todo request busque em todos os tweets as mesmas informações
    Processamento via signals
    """
    """
    Cronologicamente o ultimo tweet
    """
    tweet_mais_novo = models.ForeignKey(Tweet, related_name="novo",
                                        on_delete=models.SET_NULL, null=True)
    """
    Cronologicamente o primeiro tweet
    """
    tweet_mais_antigo = models.ForeignKey(Tweet, related_name="antigo",
                                          on_delete=models.SET_NULL, null=True)
    numero_total_tweets = models.IntegerField()

    numero_parlamentares_sem_perfil = models.IntegerField()

    @classmethod
    def processa_atual_info(self):
        mais_novo_ou_none = TweetsInfo.objects.all().last()
        return mais_novo_ou_none


class Pressao(models.Model):

    proposicao = models.ForeignKey(Proposicao, on_delete=models.SET_NULL, null=True)
    total_likes = models.IntegerField(null=False, default=0)
    total_tweets = models.IntegerField(null=False)
    total_usuarios = models.IntegerField(null=False)
    total_engajamento = models.IntegerField(null=False)
    data_consulta = models.DateTimeField(null=False)

    def get_tweets(self):
        intervalo_dias = 2
        # data_final = datetime.strftime(
        #     self.data_consulta, "%Y-%m-%d")
        data_final = self.data_consulta
        data_inicio = data_final - timedelta(days=intervalo_dias)
        data_range = [data_inicio, data_final]
        return Tweet.objects.filter(proposicao=self.proposicao).filter(data_criado__range=data_range)

    def save(self, *args, **kwargs):
        if not self.pk:
            tweets = self.get_tweets()
            metrics = tweets.values('likes', 'retweets', 'respostas')
            tweets.values('likes')
            tweets.values('retweets')
            tweets.values('respostas')
            self.total_tweets = tweets.count()
            self.total_usuarios = tweets.values('id_author').distinct().count()
            self.total_likes = metrics.aggregate(sum=Sum('likes'))['sum']
            self.total_engajamento = metrics.aggregate(sum=Sum('likes'))['sum'] + metrics.aggregate(
                sum=Sum('retweets'))['sum'] + metrics.aggregate(sum=Sum('respostas'))['sum']
        super(Pressao, self).save(*args, **kwargs)


class Engajamento(models.Model):
    # interesse = models.CharField() string
    perfil = models.ForeignKey(
        ParlamentarPerfil, on_delete=models.CASCADE, null=True, blank=True)
    tid_author = models.CharField(null=False, max_length=40, default=0)

    proposicao = models.ForeignKey(Proposicao, on_delete=models.CASCADE, default=None)
    data_consulta = models.DateTimeField(null=False)
    total_engajamento = models.IntegerField(null=False)

    def get_tweets(self):
        intervalo_dias = 2
        data_inicio = self.data_consulta - timedelta(days=intervalo_dias)
        data_range = [data_inicio, self.data_consulta]
        return Tweet.objects.filter(author=self.perfil).filter(proposicao=self.proposicao).filter(data_criado__range=data_range)

    def save(self, *args, **kwargs):
        if not self.pk:
            tweets = self.get_tweets()
            if(not tweets.count()):
                raise Exception('Não possui tweets.')
            metricas = tweets.values('likes', 'retweets', 'respostas')
            self.total_engajamento = 0
            for metrica in ['likes', 'retweets', 'respostas']:
                self.total_engajamento = self.total_engajamento + \
                    metricas.aggregate(sum=Sum(metrica))['sum']

        super(Engajamento, self).save(*args, **kwargs)
