from tweets.models import Engajamento, ParlamentarPerfil, Pressao, Proposicao, Tweet
from rest_framework import serializers


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['proposicao', 'author', 'id_author', 'id_tweet',
                  'text', 'data_criado',  'likes', 'retweets', 'respostas']


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
        model = Engajamento
        fields = [
            'data_consulta',
            'total_engajamento',
        ]


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
