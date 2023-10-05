# compute reads length distribution from a fastq file
awk 'NR%4 == 2 {lengths[length($0)]++} END {for (l in lengths) {print l, lengths[l]}}'  file.fastq

# Extract transcript id from gtf
cat file.gtf | awk '$3 == "transcript" { print $12 }' | sed 's/"//' | sed 's/";//'

