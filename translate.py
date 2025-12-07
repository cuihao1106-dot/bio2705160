# Import necessary modules from Biopython
from Bio import SeqIO
from Bio.Data import CodonTable
import os
import glob


def translate_dna_files(input_files, table_number=2):

    # 1. Define the translation table
    try:
        translation_table = CodonTable.unambiguous_dna_by_id[table_number]
        print(f"--- Using NCBI Translation Table {table_number}: {translation_table.names[0]} ---")
    except KeyError:
        print(f"Error: Translation table ID {table_number} not found.")
        return

    # 2. Iterate through each full input DNA file path
    for input_filepath in input_files:
        try:
            # Get the directory of the input file
            input_dir = os.path.dirname(input_filepath)
            # Get the filename only (e.g., 'A.fasta')
            input_filename_only = os.path.basename(input_filepath)
            # Get the base name without extension (e.g., 'A')
            base_name = os.path.splitext(input_filename_only)[0]

            # Construct the output filename: amino_A.fasta, saved in the same directory
            output_filename = os.path.join(input_dir, f"amino_{base_name}.fasta")

            print(f"\nProcessing {input_filename_only}...")

            # List to store the translated sequence records
            amino_acid_records = []

            # 3. Read the DNA sequences from the input FASTA file
            for record in SeqIO.parse(input_filepath, "fasta"):
                dna_sequence = record.seq

                if not dna_sequence:
                    print(f"Warning: Sequence '{record.id}' is empty. Skipping.")
                    continue

                # 4. Translate the DNA sequence using table 2
                amino_acid_sequence = dna_sequence.translate(table=table_number, to_stop=False)

                # 5. Create a new SeqRecord for the amino acid sequence
                amino_record = record
                amino_record.seq = amino_acid_sequence
                amino_record.description = f"Translated from DNA - {record.description}"

                amino_acid_records.append(amino_record)

            # 6. Save the translated amino acid sequences to the new output FASTA file
            if amino_acid_records:
                with open(output_filename, "w") as output_handle:
                    SeqIO.write(amino_acid_records, output_handle, "fasta")
                print(f"Successfully translated {len(amino_acid_records)} sequence(s) and saved to {output_filename}")
            else:
                print(f"No sequences were translated from {input_filename_only}.")

        except FileNotFoundError:
            print(f"Error: Input file '{input_filepath}' not found. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred while processing {input_filepath}: {e}")


# ----------------------------------------------------------------------
# --- Main execution block ---
if __name__ == "__main__":
    # Define the target directory path
    # Use 'r' before the string (raw string) for clean Windows path handling
    INPUT_DIR = r"C:\Users\hp\Desktop\seq"

    # Define the desired translation table
    NCBI_TABLE_ID = 2

    # Use glob.glob to find all files in the directory ending with .fasta
    # glob.glob returns a list of full paths (e.g., C:\Users\hp\Desktop\seq\A.fasta)
    dna_files_to_process = glob.glob(os.path.join(INPUT_DIR, "*.fasta"))

    # Check if any files were found
    if not dna_files_to_process:
        print(f"Error: No .fasta files found in the directory: {INPUT_DIR}")
    else:
        print(f"Found {len(dna_files_to_process)} FASTA file(s) to process.")
        # Run the translation function
        translate_dna_files(dna_files_to_process, table_number=NCBI_TABLE_ID)