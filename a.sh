#!/bin/bash

# Define the list of input FASTQ files
INPUT_FILES=("sampleA_part1.FASTQ" "sampleA_part2.FASTQ" "sampleA_part3.FASTQ")

# Define the output FASTA file name
OUTPUT_FILE="sampleA.fasta"

# Define the desired FASTA header
FASTA_HEADER=">SampleA_merged_reads"

# --- Main Script ---

# 1. Start the output file with the FASTA header
echo "${FASTA_HEADER}" > "${OUTPUT_FILE}"

# 2. Loop through each FASTQ file to extract and clean the read sequence
for file in "${INPUT_FILES[@]}"; do
    # Check if the file exists before processing
    if [ -f "$file" ]; then
        # Use awk to print only the second line of the FASTQ record (the sequence line),
        # and use gsub() to remove all whitespace BEFORE printing.
        awk '
            (NR % 4) == 2 { 
                gsub(/[[:space:]]/, "", $0); 
                printf "%s", $0  
            } 
        ' "$file" >> "${OUTPUT_FILE}"
        
    else
        echo "Warning: Input file not found: ${file}" >&2
    fi
done

# 3. Append a single newline character at the very end to ensure the file is correctly terminated
echo "" >> "${OUTPUT_FILE}"
