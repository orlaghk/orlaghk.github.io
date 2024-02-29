
'''import pandas as pd

# Load the CSV files into pandas DataFrames
wiki_beeswarm_df = pd.read_csv('wiki_beeswarm.csv')
new_peoples_beeswarm_df = pd.read_csv('new_peoples_beeswarm.csv')

# Align the order of columns in both DataFrames
new_peoples_beeswarm_df = new_peoples_beeswarm_df[wiki_beeswarm_df.columns]

# Iterate over each row in new_peoples_beeswarm_df
for index, row in new_peoples_beeswarm_df.iterrows():
    # Check if the 'author' column in the current row exists in wiki_beeswarm_df
    if row['author'] in wiki_beeswarm_df['author'].values:
        # Replace the row in new_peoples_beeswarm_df with the corresponding row in wiki_beeswarm_df
        new_peoples_beeswarm_df.at[index, 'urls'] = wiki_beeswarm_df[wiki_beeswarm_df['author'] == row['author']]['urls'].iloc[0]

# Write the modified new_peoples_beeswarm_df to a new CSV file
new_peoples_beeswarm_df.to_csv('updated_new_peoples_beeswarm.csv', index=False)
'''
'''
import pandas as pd
import json

def is_json_parseable(data):
    try:
        json.loads(data)
        return True
    except ValueError as e:
        return False

def fix_json_format(data):
    # Check if the data can be converted to JSON array
    try:
        json_obj = json.loads(data)
        # If the data is already a valid JSON array, return it
        if isinstance(json_obj, list):
            return data
    except ValueError as e:
        pass

    # If the data is not in JSON array format, fix the format
    # Remove single quotes, escape any existing double quotes and add square brackets
    data = data.replace("'", "") # Remove single quotes
    data = data.replace('\\"', '\\\\"') # Escape any existing double quotes
    data = '[' + data + ']' # Add square brackets to enclose the list
    return data

# Read the CSV file
df = pd.read_csv("updated_new_peoples_beeswarm.csv")
df = df.head(100)

# Check if the 'titles' column is in JSON parseable format and fix the format if needed
df['titles'] = df['titles'].apply(lambda x: x if is_json_parseable(x) else fix_json_format(x))

# Save the updated dataframe to a new CSV file
df.to_csv("updated_new_beeswarm_fixed.csv", index=False)
'''

import pandas as pd

# Read in the CSV file
df = pd.read_csv('subject_tf_fraction_by_decade_with_occurrences.csv')

# Define a function to change the format of the decade values
def change_decade_format(decade):
    # If the decade is a string, remove the "[" and ")" characters, and replace "," with "-"
    if isinstance(decade, str):
        start, end = map(int, decade[1:-1].split(', '))
        return f"{start}-{end}"
    else:
        return decade

# Apply the function to the 'decade' column
df['decade'] = df['decade'].apply(change_decade_format)

# Write the updated data to a new CSV file
df.to_csv('updated_subject_tf_fraction_by_decade_with_occurrences.csv', index=False)
