def cria_sigla(etapa):
    sigla = str(
        etapa.sigla_tipo + ' ' +
        str(etapa.numero) + '/' +
        str(etapa.data_apresentacao.year)
    )
    return sigla
