"""
This code obtains stas needed for the Main.py.
We need the following:
    average
    
"""

import pandas as pd
from pathlib import Path

def getAveragePrice():
    input_dir = Path("cleaned")

    for file_type in ["prices"]:
        for day_num in range(3):  # Days 0-2

            # Adjust day_num for file naming convention
            if day_num != 0:
                day_num = -day_num
            
            # Build input/output paths
            input_file = input_dir / f"cleaned_{file_type}_round_1_day_{day_num}.csv"
            
    # Load data into a DataFrame
    df = pd.read_csv(input_file)
    
    # Drop the following columns:
    df = df[['day', 'timestamp', 'product', 'bid_price_1', 'ask_price_1', 'mid_price']]
    
    # Create a new column 'spread', difference between ask_price_1 and bid_price_1.
    df['spread'] = df['ask_price_1'] - df['bid_price_1']
    
    # Group by product 
    # Calculate average mid_price for each product.
    avg_mid_price = df.groupby('product')['mid_price'].mean()
    # Calculate average spread for each product.
    avg_spread = df.groupby('product')['spread'].mean()
    
    # Merge these two Series into a DataFrame for better overview.
    averages = pd.DataFrame({
        'avg_mid_price': avg_mid_price,
        'avg_spread': avg_spread
    })

    #output = averages
    
    #print(averages)
    
    '''
    output will be like this:
                        avg_mid_price  avg_spread
    product
    KELP                 2011.76200      2.6922
    RAINFOREST_RESIN    10000.00350      6.7288
    SQUID_INK            2033.94805      2.7177
    '''

    output = averages.drop(columns=['avg_spread'])

    # print(output)
    '''
    The output will be like this:
                        avg_mid_price
    product
    KELP                 2011.76200
    RAINFOREST_RESIN    10000.00350
    SQUID_INK            2033.94805
    '''
    return output

    
# getAveragePrice()

print("\nAverage price provided\n")

def getAverageSpread():
    df = getAveragePrice()
    if df is not None:
        # Keep only avg_mid_price column
        output = df[['avg_mid_price']]  # Note: Double brackets to keep as DataFrame
        #print("\nAverage Mid Prices (Spread Removed):")
        #print(output)

        '''
        Output will be like this:
                            avg_mid_price
        product
        KELP                 2011.76200
        RAINFOREST_RESIN    10000.00350
        SQUID_INK            2033.94805
        '''
        return output
    else:
        return None

getAverageSpread()

print("\nAverage spread provided\n")