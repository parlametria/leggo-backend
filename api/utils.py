from datetime import datetime, timedelta
from api.models import TemperaturaHistorico, PautaHistorico


def get_time_filtered_temperatura(request):
    semanas_anteriores = request.query_params.get('semanas_anteriores')
    data_referencia = request.query_params.get('data_referencia')

    queryset = TemperaturaHistorico.objects

    date = None
    if data_referencia:
        try:
            date = datetime.strptime(data_referencia, '%Y-%m-%d')
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
        else:
            queryset = queryset.filter(periodo__lte=date)

    if semanas_anteriores:
        if not date:
            date = datetime.today()
        start_date = date - timedelta(weeks=int(semanas_anteriores))
        queryset = queryset.filter(periodo__gte=start_date)

    if not data_referencia and not semanas_anteriores:
        return queryset.filter()
    else:
        return queryset


def get_time_filtered_pauta(request):
    data_referencia = request.query_params.get('data_referencia')

    queryset = PautaHistorico.objects

    if data_referencia:
        try:
            date = datetime.strptime(data_referencia, '%Y-%m-%d')
            semana_atual = date.isocalendar()[1]
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            semana_atual = datetime.today().isocalendar()[1]
        return queryset.filter(semana=semana_atual)
    else:
        return queryset.filter()
