import pandas as pd

# Read the peoples_beeswarm DataFrame
df = pd.read_csv("odnb_beeswarm.csv")
df_creator = pd.read_csv("odnb_beeswarm copy.csv")

# Merge the DataFrames based on the 'titles' column
merged_df = pd.merge(df, df_creator[['title', 'cleaned_creator']], 
                     on='title', 
                     how='left')

# Rename the 'cleaned_creator' column to avoid duplicate columns
merged_df.rename(columns={'cleaned_creator': 'matched_cleaned_creator'}, inplace=True)

merged_df.to_csv("odnb_beeswarm_with_matched_creator.csv", index=False)
