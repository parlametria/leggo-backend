from rest_framework import serializers
from api.model.temperatura_historico import TemperaturaHistorico


class TemperaturaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturaHistorico
        fields = ('periodo', 'temperatura_recente', 'temperatura_periodo')
