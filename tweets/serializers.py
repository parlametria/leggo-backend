from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao, Tweet, TweetsInfo
from rest_framework import serializers
from django.db import models


class ParlamentarPerfilSerializer(serializers.HyperlinkedModelSerializer):
    # entidade = serializers.RelatedField(read_only=True)
    entidade = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParlamentarPerfil
        fields = (
            'twitter_id',
            'is_personalidade',
            'name',
            'entidade',
        )


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    # author = ParlamentarPerfilSerializer(many=False)

    class Meta:
        model = Tweet
        fields = ['id_author', 'id_tweet',
                  'text_html', 'data_criado',  'likes', 'retweets', 'respostas']


class TweetInteressesSerializer(serializers.Serializer):
    interesse = models.CharField(max_length=30)
    tweets = TweetSerializer(many=True)


class PressaoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pressao
        fields = [
            'total_likes',
            'total_tweets',
            'total_usuarios',
            'total_engajamento',
            'data_consulta',
        ]


class EngajamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EngajamentoProposicao
        fields = [
            'data_consulta',
            'total_engajamento',
        ]


class TweetsInfoSerializer(serializers.HyperlinkedModelSerializer):

    tweet_mais_novo = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='data_criado'
    )

    tweet_mais_antigo = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='data_criado'
    )

    class Meta:
        model = TweetsInfo
        fields = (
            'tweet_mais_novo',
            'tweet_mais_antigo',
            'numero_total_tweets',
            'numero_parlamentares_sem_perfil',
        )
