def get_nome_partido_uf(casa, bancada, nome, partido, uf):
    tipo_parlamentar = ''
    marcador_bancada = ''

    if (uf == 'nan'):
        uf = '-'

    if (partido == 'nan'):
        partido = '-'

    if (casa == 'camara'):
        tipo_parlamentar = 'Dep. '
    elif (casa == 'senado'):
        tipo_parlamentar = 'Sen. '
    else:
        tipo_parlamentar = ''

    if (bancada == 'oposição'):
        marcador_bancada = '* '

    descricao_parlamentar = marcador_bancada + tipo_parlamentar + \
        nome + ' (' + partido + '/' + uf + ')'

    return(descricao_parlamentar)
