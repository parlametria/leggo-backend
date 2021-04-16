def queryPressaoOitoDias(interesse):

    p = f"SELECT DISTINCT ON (p.id_leggo) \
            1 AS id, \
            aux_top.id_leggo, \
            trends_max_popularity, \
            pressao_oito_dias \
            FROM  api_pressao p \
            INNER JOIN \
            (SELECT DISTINCT(id_leggo) \
            FROM api_interesse \
            WHERE interesse = '{interesse}') AS interesse_aux \
            ON p.id_leggo = interesse_aux.id_leggo \
            LEFT JOIN \
            (WITH summary AS ( \
                SELECT p.id_leggo,  \
                    p.trends_max_popularity AS pressao_oito_dias,  \
                    ROW_NUMBER() OVER(PARTITION BY p.id_leggo  \
                                            ORDER BY p.date DESC) AS rk \
                FROM api_pressao p) \
            SELECT s.* \
            FROM summary s \
            WHERE s.rk = 2) AS aux_top  ON \
            aux_top.id_leggo = p.id_leggo \
            ORDER  BY p.id_leggo, p.date DESC;"

    return p
