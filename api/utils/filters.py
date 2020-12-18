from datetime import datetime, timedelta
from django.db.models import Q
from api.model.pauta_historico import PautaHistorico
from api.model.interesse import Interesse
from api.model.destaques import Destaques


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
        end_date = date + timedelta(days=8)
        queryset = queryset.filter(data__lte=end_date)
    else:
        queryset = queryset.filter(data__week=date.isocalendar()[1],
                                   data__year=date.isocalendar()[0])

    return queryset


def get_filtered_interesses(interesseArg, temaArg=None):
    '''
    Filtra interesses e temas a partir da string do interesse passado como parâmetro.
    Caso o tema esteja vazio, ou inexistente, a função retorna
    apenas o filtro para interesses.
    '''
    if interesseArg is None:
        return Interesse.objects

    if temaArg is None:
        return Interesse.objects.filter(interesse=interesseArg)

    return Interesse.objects.filter(interesse=interesseArg,
                                    tema_slug__contains=temaArg)


def get_filtered_destaques(destaquesArg):
    '''
    Retorna ids das proposições em destaque
    '''

    return (Destaques.objects.filter(Q(criterio_avancou_comissoes=True) |
                                     Q(criterio_aprovada_em_uma_casa=True))
            .values('id_leggo'))


def get_filtered_autores(request, queryset):
    '''
    Filtra os autores que apresentaram documentos em comissões ou plenário
    '''
    is_important = request.query_params.get('is_important')
    if not is_important:
        return queryset.filter()

    return queryset.filter(is_important=is_important)
