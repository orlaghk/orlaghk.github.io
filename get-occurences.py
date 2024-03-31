# import pandas as pd
# import ast

# # Load the CSV file into a DataFrame
# df = pd.read_csv('title_tfidf_stemmed_by_decade_with_occurrences.csv')

# # Convert the 'occurrences' column from string to list of integers
# df['occurrences'] = df['occurrences'].apply(lambda x: ast.literal_eval(x))

# # Find the top 80 words for each decade
# top_words = df.groupby('decade').apply(lambda x: x.nlargest(80, 'tfidf')).reset_index(drop=True)

# # Explode the 'occurrences' column to get a row for each occurrence
# top_words_exploded = top_words.explode('occurrences')

# # Drop duplicates based on the 'occurrences' column
# top_words_unique_occurrences = top_words_exploded.drop_duplicates('occurrences')

# # Read the existing CSV file to get the current occurrences
# existing_occurrences = pd.read_csv('all_the_df_occurrences.csv')

# # Filter out occurrences that are already in the DataFrame
# new_occurrences = top_words_unique_occurrences[~top_words_unique_occurrences['occurrences'].isin(existing_occurrences['occurrences'])]

# # Append the new unique occurrences to the existing CSV file
# new_occurrences.to_csv('all_tfidf_the_df_occurrences.csv', mode='a', index=False, header=False, columns=['occurrences'])

import pandas as pd

# Read in the first CSV file
df1 = pd.read_csv('all_tfidf_the_df_occurrences.csv')

# Read in the second CSV file
df2 = pd.read_csv('all_the_df_occurrences.csv')

# Combine the 'occurrences' columns by merging unique values
combined_occurrences = pd.concat([df1['occurrences'], df2['occurrences']]).drop_duplicates().reset_index(drop=True)

# Create a new DataFrame with the combined 'occurrences' column
combined_df = pd.DataFrame({'occurrences': combined_occurrences})

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_file.csv', index=False)

# Display the combined DataFrame
print(len(combined_df))
