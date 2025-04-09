"""
This script reads a CSV file with semicolon delimiters and writes it to a new CSV file with comma delimiters.
"""
import csv
from pathlib import Path

# Configuration
input_dir = Path("round-1-island-data-bottle")
output_dir = Path("formatted")
output_dir.mkdir(exist_ok=True)  # Create output directory

# Process all combinations of rounds/days/file types
for file_type in ["prices", "trades"]:
    for day_num in range(3):  # Days 0-2

        # Adjust day_num for file naming convention
        if day_num != 0:
            day_num = -day_num
        
        # Build input/output paths
        input_file = input_dir / f"{file_type}_round_1_day_{day_num}.csv"
        output_file = output_dir / f"formatted_{file_type}_round_1_day_{day_num}.csv"

        # Process if input file exists
        if input_file.exists():
            with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
                 open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                
                reader = csv.reader(infile, delimiter=';')
                writer = csv.writer(outfile, delimiter=',')
                
                # Process each row
                for row in reader:
                    # Add your formatting logic here before writing
                    formatted_row = row  # Replace with actual formatting
                    writer.writerow(formatted_row)
            
            print(f"Processed: {input_file.name} → {output_file.name}")
        else:
            print(f"Missing file: {input_file.name}")
