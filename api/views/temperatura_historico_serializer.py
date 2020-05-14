from django.db.models import Max
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from datetime import datetime
from api.model.temperatura_historico import TemperaturaHistorico
from rest_framework import status


class TemperaturaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturaHistorico
        fields = ('periodo', 'temperatura_recente', 'temperatura_periodo')


class TemperaturaMaxPeriodo(APIView):
    '''
    Calcula a temperatura máxima entre as proposições de um interesse.
    Pode receber como parâmetro o intervalo de tempo usado para o cálculo.
    '''

    def get(self, request, format=None):

        interesseArg = self.request.query_params.get('interesse', 'leggo')
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        data_inicio_processada = None
        data_fim_processada = None

        try:
            if data_inicio is not None:
                data_inicio_processada = datetime.strptime(data_inicio, '%Y-%m-%d')
        except ValueError:
            return JsonResponse(
                {'error': f'Data de início ({data_inicio}) inválida.'
                 'Formato correto: yyyy-mm-dd'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            data_fim_processada = (
                datetime.today() if data_fim is None else datetime.strptime(
                    data_fim, '%Y-%m-%d'))
        except ValueError:
            print(
                f'Data de fim ({data_fim}) inválida. '
                'Utilizando data atual como data de fim.')
            data_fim_processada = datetime.today()

        queryset = TemperaturaHistorico.objects.filter(
            proposicao__interesse__interesse=interesseArg)

        if data_inicio_processada is not None:
            queryset = queryset.filter(periodo__gte=data_inicio_processada)

        queryset = queryset.filter(periodo__lte=data_fim_processada)

        queryset = queryset.aggregate(max_temperatura_periodo=Max('temperatura_recente'))

        return JsonResponse(queryset, status=status.HTTP_200_OK)
