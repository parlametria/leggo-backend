def get_destaque_query(destaque):
  q_destaque = ""
  if destaque == "true":
    q_destaque = (
      f" AND id_leggo IN (SELECT DISTINCT(id_leggo) \
        FROM api_destaques \
        WHERE casa_req_urgencia_aprovado = 'true' \
        OR criterio_req_urgencia_apresentado = 'true' \
        OR criterio_aprovada_em_uma_casa = 'true')"
    )
  return q_destaque

def get_tema_query(tema):
  q_tema = ''
  
  if tema:
    temaArg = tema.center(len(tema) + 4, '%') if tema else '%%'
    q_tema = (
    f" AND interesse.tema_slug LIKE '{temaArg}'"
    )

  return q_tema


def get_tipo_documento_query(tipo_documento):
  q_tipo_documento = ''

  if tipo_documento:
    documentoArg = tipo_documento.center(len(tipo_documento) + 4, '%') if tipo_documento else '%%'
    q_tipo_documento = (
    f" AND tipo_documento LIKE '{documentoArg}'"
    )
  return q_tipo_documento


def queryAutoriasAgregadas(data_inicio, interesse, tema, destaque):
  q_tema = get_tema_query(tema)
  q_destaque = get_destaque_query(destaque)

  if tema:
    q_destaque = ''

  q = (
    f"SELECT \
    1 as id, \
    autoria.id_autor_parlametria, \
    autoria.tipo_acao, \
    COUNT(autoria.tipo_acao) AS num_documentos, \
    SUM(autoria.peso_autor_documento) AS peso_total, \
    ROW_NUMBER() OVER ( \
    PARTITION BY tipo_acao \
    ORDER BY COUNT(tipo_acao) DESC) \
    AS ranking_documentos \
    FROM ( \
      SELECT \
        DISTINCT(id_documento), \
        id_autor_parlametria, \
        tipo_acao, \
        peso_autor_documento \
      FROM api_autoria \
      WHERE data >= '{data_inicio}' AND id_leggo IN ( \
        SELECT interesse.id_leggo \
        FROM api_interesse as interesse \
        WHERE interesse.interesse = '{interesse}' \
        {q_tema}) \
      {q_destaque} \
      GROUP BY id_autor_parlametria, id_documento, tipo_acao, peso_autor_documento \
    ) AS autoria  \
    GROUP BY id_autor_parlametria, tipo_acao \
    ORDER BY ranking_documentos ASC, tipo_acao ASC;" \
  )

  return q

def queryAutoriasAgregadasByTipoAcao(data_inicio, interesse, tema, destaque, tipo_acao_filtro, tipo_documento=None):
  q_tema = get_tema_query(tema)
  q_destaque = get_destaque_query(destaque)
  q_tipo_documento = get_tipo_documento_query(tipo_documento)

  if tema:
    q_destaque = ''

  tipoArg = tipo_acao_filtro.center(len(tipo_acao_filtro) + 4, '%')
  
  q = (
    f"SELECT \
    1 as id, \
    id_autor_parlametria, \
    id_autor, \
    COUNT(DISTINCT(id_documento)) AS quantidade_autorias, \
    SUM(peso_autor_documento) AS peso_documentos \
    FROM ( \
      SELECT \
        DISTINCT(id_documento), \
        id_autor_parlametria, \
        id_autor, \
        peso_autor_documento \
      FROM api_autoria \
      WHERE data >= '{data_inicio}' AND id_leggo IN ( \
        SELECT interesse.id_leggo \
        FROM api_interesse as interesse \
        WHERE interesse.interesse = '{interesse}' \
        {q_tema}) \
        {q_destaque} \
        AND tipo_acao LIKE '{tipoArg}' \
        {q_tipo_documento} \
      GROUP BY id_autor_parlametria, id_autor, id_documento, peso_autor_documento \
    ) AS autoria  \
    GROUP BY id_autor_parlametria, id_autor;" \
  )

  return q


def queryAutoriasAgregadasByTipoAcaoEIdAutor(data_inicio, interesse, tema, destaque, id_autor, tipo_acao_filtro, tipo_documento=None):
  core_query = queryAutoriasAgregadasByTipoAcao(data_inicio, interesse, tema, destaque, tipo_acao_filtro, tipo_documento)

  q = (
    f"SELECT \
      1 as id, \
       * \
      FROM (SELECT \
      autoria_agg.*, \
      MAX(quantidade_autorias) OVER (ORDER BY quantidade_autorias DESC) AS max_quantidade_autorias, \
      MIN(quantidade_autorias) OVER (ORDER BY quantidade_autorias ASC) AS min_quantidade_autorias \
      FROM ({core_query[:-1]}) AS autoria_agg) AS autoria_agregada_autor \
      WHERE id_autor_parlametria = {id_autor};")
  return q