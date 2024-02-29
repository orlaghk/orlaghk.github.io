'''import pandas as pd
import ast

# Load the CSV file into a DataFrame
df = pd.read_csv('retry_subject_tf_fraction_by_decade_with_occurrences.csv')

# Convert the 'occurrences' column from string to list of integers
df['occurrences'] = df['occurrences'].apply(lambda x: ast.literal_eval(x))

# Find the top 80 words for each decade
top_words = df.groupby('decade').apply(lambda x: x.nlargest(80, 'tf')).reset_index(drop=True)

# Explode the 'occurrences' column to get a row for each occurrence
top_words_exploded = top_words.explode('occurrences')

# Drop duplicates based on the 'occurrences' column
top_words_unique_occurrences = top_words_exploded.drop_duplicates('occurrences')

# Save the result to a new CSV file
top_words_unique_occurrences.to_csv('unique_occurrences.csv', index=False, columns=['occurrences'])
'''
import pandas as pd
import ast

# Load the CSV file into a DataFrame
df = pd.read_csv('title_rs_tf_fraction_by_decade_with_occurrences.csv')

# Convert the 'occurrences' column from string to list of integers
df['occurrences'] = df['occurrences'].apply(lambda x: ast.literal_eval(x))

# Find the top 80 words for each decade
top_words = df.groupby('decade').apply(lambda x: x.nlargest(80, 'tf')).reset_index(drop=True)

# Explode the 'occurrences' column to get a row for each occurrence
top_words_exploded = top_words.explode('occurrences')

# Drop duplicates based on the 'occurrences' column
top_words_unique_occurrences = top_words_exploded.drop_duplicates('occurrences')

# Read the existing CSV file to get the current occurrences
existing_occurrences = pd.read_csv('cleaned_df_occurrences.csv')

# Filter out occurrences that are already in the DataFrame
new_occurrences = top_words_unique_occurrences[~top_words_unique_occurrences['occurrences'].isin(existing_occurrences['occurrences'])]

# Append the new unique occurrences to the existing CSV file
new_occurrences.to_csv('cleaned_df_occurrences.csv', mode='a', index=False, header=False, columns=['occurrences'])
