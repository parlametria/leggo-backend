from django.db import models
from api.model.entidade import Entidade
from api.model.etapa_proposicao import Proposicao
from datetime import timedelta
from django.db.models import Sum


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


class Tweet(models.Model):

    proposicao = models.ManyToManyField(Proposicao)
    # interesse = models.TextField()
    author = models.ForeignKey(ParlamentarPerfil, related_name="author",
                               on_delete=models.SET_NULL, null=True, blank=True)

    id_author = models.CharField(null=False, max_length=40, default=0)
    id_tweet = models.CharField(null=False, max_length=40, default=0)

    text = models.TextField()
    text_html = models.TextField()

    data_criado = models.DateField(null=False)

    likes = models.IntegerField(null=False)
    retweets = models.IntegerField(null=False)
    respostas = models.IntegerField(null=False)


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

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.SET_NULL, null=True, related_name='pressao_intervalo')
    total_likes = models.IntegerField(null=False, default=0)
    total_tweets = models.IntegerField(null=False)
    total_usuarios = models.IntegerField(null=False)
    total_engajamento = models.IntegerField(null=False)
    data_consulta = models.DateField(null=False)

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


class EngajamentoProposicao(models.Model):
    # interesse = models.CharField() string
    perfil = models.ForeignKey(
        ParlamentarPerfil, on_delete=models.CASCADE, null=True, blank=True)
    tid_author = models.CharField(null=False, max_length=40, default=0)

    proposicao = models.ForeignKey(Proposicao, on_delete=models.CASCADE, default=None)
    data_consulta = models.DateField()
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

        super(EngajamentoProposicao, self).save(*args, **kwargs)
