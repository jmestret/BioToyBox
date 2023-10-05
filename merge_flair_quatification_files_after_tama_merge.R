# Packages
library(tidyverse)
library(stringr)

# Input
args <- commandArgs(trailingOnly = TRUE)
quantification_fofn <- args[1]
old_2_new_id_tama <- args[2]
out_file <- args[3]

quantification_fofn <- readLines(quantification_fofn)
old_2_new_id_tama <- read.table(old_2_new_id_tama, header = F, sep = "\t")

# Format TAMA merge dataframe
old_2_new_id_tama <- as.data.frame(
  stringr::str_split_fixed(old_2_new_id_tama[, 4], pattern = ";|_", 3)
)
colnames(old_2_new_id_tama) <- c("new_id", "sample_id", "old_id")

# Change old transcript id to merged transcript id
quant_mat_list <- list()
for (i in 1:length(quantification_fofn)) {
  quant_file <- read.table(quantification_fofn[i], header = TRUE, sep = "\t")
  quant_file[,c("trans_id", "gene_id")] <- stringr::str_split_fixed(quant_file$ids, pattern = "_\\s*(?=[^_]+$)|_(?=chr)", 2)
 
  sample_id <- strsplit(colnames(quant_file)[2], "_")[[1]][1]
  tama_name_by_sample <- old_2_new_id_tama[old_2_new_id_tama$sample_id == sample_id,]
  match_ids <- match(quant_file$trans_id, tama_name_by_sample$old_id)
  quant_file$transcript_id <- tama_name_by_sample$new_id[match_ids]
  
  quant_file <- subset(quant_file, select = -c(ids, trans_id, gene_id))
  quant_mat_list[[i]] <- quant_file
}

# Merge quantification matrices
quant_merged_matrix <- quant_mat_list %>%
  reduce(full_join, by = "transcript_id") %>%
  replace(is.na(.), 0) %>% 
  relocate(transcript_id)

# Write output
write.table(quant_merged_matrix, file = out_file,
            sep = "\t", col.names = T, row.names = F, quote = F)











