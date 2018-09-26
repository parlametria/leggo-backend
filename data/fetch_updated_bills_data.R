#!/usr/bin/env Rscript
library(magrittr)
library(dplyr)

args = commandArgs(trailingOnly = TRUE)

MIN_NUM_ARGS = 3

if (length(args) < MIN_NUM_ARGS) {
    stop(paste("Wrong number of arguments!",
               "Usage: Rscript fetch_updated_bills_data.R <pls_ids_filepath> <tmp_csvs_folderpath> <mapeamento_pls_id_filepath>",sep="\n"))
}


pls_ids_filepath = args[1]
tmp_csvs_folderpath = args[2]
mapeamento_pls_id_filepath = args[3]

devtools::install_github('analytics-ufcg/agora-digital', force=TRUE)

all_pls <- readr::read_csv(pls_ids_filepath)
mapeamento_pls_id <- readr::read_csv(mapeamento_pls_id_filepath)
 
process_pl <- function(id, casa, tema, apelido, mapeamento_df) {
  print(paste("Processando id",id,"da casa",casa))
  prop <- agoradigital::fetch_proposicao(id, casa, apelido, tema, TRUE)
  tram <- agoradigital::fetch_tramitacao(id,casa,TRUE)
  proc_tram <- agoradigital::process_proposicao(prop,tram,casa)%>%
    mutate(data_hora = as.POSIXct(data_hora))
  status <- agoradigital::extract_status_tramitacao(tram)
  energia_value <- agoradigital::get_energia(proc_tram)
  progresso_pl <- agoradigital::get_progresso(mapeamento_df, tram, prop, casa)
  extended_prop <- merge(prop,status,by="prop_id") %>%
    dplyr::mutate(energia = energia_value)
  
  pl_data <- list(proposicao = extended_prop, 
                  fases_eventos = proc_tram,
                  progresso = progresso_pl)
}

res <- purrr::pmap(list(all_pls$id, all_pls$casa, all_pls$apelido, all_pls$tema), function(x, y, z, w, df) process_pl(x, y, z, w, mapeamento_pls_id))
proposicoes <- purrr::map_df(res, ~ .$proposicao)
tramitacoes <- purrr::map_df(res, ~ .$fases_eventos)
progressos <- purrr::map_df(res, ~ .$progresso)

proposicoes$ano <- NULL

names(proposicoes) <- c("id_ext", "casa", "sigla_tipo", "numero", "data_apresentacao", "ementa", "palavras_chave",
            "casa_origem", "autor_nome", "tema", "apelido", "regime_tramitacao", "forma_apreciacao", 
            "em_pauta", "energia")

names(tramitacoes) <- c("id_ext","casa","data","sequencia","texto_tramitacao","sigla_local",
  "id_situacao","descricao_situacao","fase","situacao_descricao_situacao",
  "evento","data_audiencia","local","global")

progressos <-
  progressos %>% dplyr::select(prop_id, casa, fase_global, local, data_inicio, data_fim)
names(progressos) <- c("id_ext", "casa", "fase_global", "local", "data_inicio", "data_fim")

#progressos$data_inicio <- as.Date(progressos$data_inicio)
#progressos$data_fim <- as.Date(progressos$data_fim)
#progressos$data_inicio[is.na(progressos$data_inicio)] <- as.Date("0001jan1T00:00", "%Y%b%d")
#progressos$data_fim[is.na(progressos$data_fim)] <- as.Date("0001jan1T00:00", "%Y%b%d")
progressos$id_ext[is.na(progressos$id_ext)] <- 0
progressos$casa[is.na(progressos$casa)] <- 'None'

readr::write_csv(proposicoes,paste0(tmp_csvs_folderpath,'/proposicoes.csv'))
readr::write_csv(tramitacoes,paste0(tmp_csvs_folderpath,'/trams.csv'))
readr::write_csv(progressos,paste0(tmp_csvs_folderpath,'/progressos.csv'))


