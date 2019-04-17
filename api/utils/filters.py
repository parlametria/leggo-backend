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
    '''
    Filtra as pautas que ocorreram depois ou no dia da data_referencia. Se a
    data_referencia é uma sexta-feira, retornará todas as pautas com um
    período de 6 dias após, se não,retorna as pautas da mesma semana da data_referencia.
    '''
    data_referencia = request.query_params.get('data_referencia')

    queryset = PautaHistorico.objects

    if not data_referencia:
        return queryset.filter()

    date = datetime.strptime(data_referencia, '%Y-%m-%d')
    queryset = queryset.filter(data__gte=date)

    if(date.weekday() == 4):  # friday
        end_date = date + timedelta(days=6)
        queryset = queryset.filter(data__lte=end_date)
    else:
        queryset = queryset.filter(data__week=date.isocalendar()[1],
                                   data__year=date.isocalendar()[0])

    return queryset
