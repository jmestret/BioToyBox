# gc_content_and_length.R

# Packages
library(rtracklayer)
library(Rsamtools)
library(data.table)


#' Get Transcript Length and GC Content from GTF File
#'
#' This function extracts transcript length and GC content information from a GTF file.
#'
#' @param g A path to the genome FASTA file.
#' @param a A path to a GFF/GTF file containing transcript coordinates.
#' @param a_format The format of the annotation file (default is "gtf").
#'
#' @return A data.table object with the following columns:
#'   - transcript_id: Transcript identifier
#'   - gene_id: Gene identifier
#'   - nGC: Number of GC bases in each isoform
#'   - length: Total length of the isoform (including exons and UTRs)
#'
#' @export
gc_length <- function(g, a, a_format = "gtf"){
  # Read genome and annotation
  genome <- Rsamtools::FaFile(g)
  open(genome)
  
  annotation <- rtracklayer::import.gff(a,
                                        format = a_format,
                                        genome = NA,
                                        feature.type = "exon")
  
  # Create annotation grouped by feature
  group_annot <- IRanges::reduce(split(annotation, elementMetadata(annotation)$transcript_id))
  reduced_annot <- unlist(group_annot, use.names = TRUE)
  elementMetadata(reduced_annot)$transcript_id <- rep(names(group_annot), elementNROWS(group_annot))

  # Get number of GC and feature length
  # NOTE: Length as the total length of exons plus the lengths of UTRs
  # UTRs are usually part of exons in GTF. For gene length the sum of 
  # is it better sum, mean, median or max of isoforms lengths?
  elementMetadata(reduced_annot)$nGC <- Biostrings::letterFrequency(Biostrings::getSeq(genome, reduced_annot), "GC")[,1]
  elementMetadata(reduced_annot)$length <- Biostrings::width(reduced_annot)
  
  gclength <- data.table::as.data.table(elementMetadata(reduced_annot))
  gclength <- gclength[, .(nGC = sum(nGC), length = sum(length)), by = transcript_id]
  gene_2_trans <- data.table::as.data.table(unique(elementMetadata(annotation)[c("gene_id", "transcript_id")]))
  gclength <- merge(gene_2_trans, gclength, by = "transcript_id")
  
  return(gclength)
}
