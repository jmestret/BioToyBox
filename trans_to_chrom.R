# Packages
library(rtracklayer)
library(Rsamtools)
library(data.table)

trans_to_chrom <- function(a, a_format = "gtf"){
  annotation <- rtracklayer::import.gff(a,
                                        format = a_format,
                                        genome = NA,
                                        feature.type = "exon")
  
  group_annot <- IRanges::reduce(split(annotation, elementMetadata(annotation)$transcript_id))
  reduced_annot <- unlist(group_annot, use.names = TRUE)
  t2c <- as.data.frame(reduced_annot, row.names = 1:length(reduced_annot))
  t2c$transcript_id <- names(reduced_annot)
  t2c$chrom <- t2c$seqnames
  t2c <- t2c[, c("chrom", "transcript_id")]
  t2c <- unique(t2c)
  
  return(t2c)
}