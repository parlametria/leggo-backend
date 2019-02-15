import time
from scipy import stats


def get_coefficient_temperature(temperatures):
    '''
    Calcula coeficiente linear das temperaturas nas últimas 6 semanas.
    '''
    dates_x = [datetime_to_timestamp(temperatura.periodo)
               for temperatura in temperatures[:6]]
    temperaturas_y = [temperatura.temperatura_recente for temperatura in temperatures[:6]]

    if(dates_x and temperaturas_y and len(dates_x) > 1 and len(temperaturas_y) > 1):
        return stats.linregress(dates_x, temperaturas_y)[0]
    else:
        return 0


def datetime_to_timestamp(date):
    return time.mktime(date.timetuple())
