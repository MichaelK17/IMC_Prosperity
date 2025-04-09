"""
This script cleans a CSV file, by droping unnecessary columns.

"""
import csv
from pathlib import Path
import pandas as pd

# Configuration
input_dir = Path("formatted")
output_dir = Path("cleaned")
output_dir.mkdir(exist_ok=True)  # Create output directory

# Process all combinations of rounds/days/file types
for file_type in ["prices"]:
    for day_num in range(3):  # Days 0-2

        # Adjust day_num for file naming convention
        if day_num != 0:
            day_num = -day_num
        
        # Build input/output paths
        input_file = input_dir / f"formatted_{file_type}_round_1_day_{day_num}.csv"
        output_file = output_dir / f"cleaned_{file_type}_round_1_day_{day_num}.csv"

        # Process if input file exists
        if input_file.exists():
            # Load the CSV file into a DataFrame
            df = pd.read_csv(input_file)

            # List of columns to drop
            columns_to_drop = [
                'bid_price_2', 'bid_volume_2', 'bid_price_3', 'bid_volume_3',
                'ask_price_2', 'ask_volume_2', 'ask_price_3', 'ask_volume_3'
            ]

            # Drop the specified columns
            df_cleaned = df.drop(columns=columns_to_drop)

            # Save the cleaned DataFrame back to a new CSV file
            df_cleaned.to_csv(output_file, index=False)

            print(f"Processed: {input_file.name} → {output_file.name}")
        else:
            print(f"Missing file: {input_file.name}")
