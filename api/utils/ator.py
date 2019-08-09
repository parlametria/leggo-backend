def get_nome_partido_uf(nome, partido, uf):

    if(uf == 'nan'):
        uf = ''

    if(partido == 'nan'):
        partido = ''
    barra = '' if (partido == '' or uf == '') else '/'
    return (nome + ' - ' + partido + barra + uf)
