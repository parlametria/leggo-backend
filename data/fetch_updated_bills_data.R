#!/usr/bin/env Rscript
library(magrittr)
library(dplyr)

args = commandArgs(trailingOnly = TRUE)

MIN_NUM_ARGS = 2

if (length(args) < MIN_NUM_ARGS) {
    stop(paste("Wrong number of arguments!",
               "Usage: Rscript fetch_updated_bills_data.R <pls_ids_filepath> <tmp_csvs_folderpath>",sep="\n"))
}


pls_ids_filepath = args[1]
tmp_csvs_folderpath = args[2]

devtools::install_github('analytics-ufcg/agora-digital', force=TRUE)

all_pls <- readr::read_csv(pls_ids_filepath)

process_pl <- function(id, casa, apelido) {
  print(paste("Processando id",id,"da casa",casa))
  prop <- agoradigital::fetch_proposicao(id,casa, apelido,TRUE)
  tram <- agoradigital::fetch_tramitacao(id,casa,TRUE)
  proc_tram <- agoradigital::process_proposicao(prop,tram,casa)%>%
    mutate(data_hora = as.POSIXct(data_hora))
  status <- agoradigital::extract_status_tramitacao(tram)
  energia_value <- agoradigital::get_energia(proc_tram)
  
  extended_prop <- merge(prop,status,by="prop_id") %>%
    dplyr::mutate(energia = energia_value)
  
  pl_data <- list(proposicao = extended_prop, 
                  fases_eventos = proc_tram)
}

res <- purrr::pmap(list(all_pls$id, all_pls$casa, all_pls$apelido), function(x, y, z) process_pl(x, y, z))
proposicoes <- purrr::map_df(res, ~ .$proposicao)
tramitacoes <- purrr::map_df(res, ~ .$fases_eventos)
readr::write_csv(proposicoes,paste0(tmp_csvs_folderpath,'/proposicoes.csv'))
readr::write_csv(tramitacoes,paste0(tmp_csvs_folderpath,'/trams.csv'))

