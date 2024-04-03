# getting the tf pages
'''
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import PorterStemmer

df = pd.read_csv("cleaned_df.csv")
interval_size = 50

df.dropna(subset=['date'], inplace=True)

# Calculate rounded down min and rounded up max values
date_min, date_max = df['date'].min(), df['date'].max()

rounded_down_min = interval_size * (int(date_min) // interval_size)
rounded_up_max = interval_size * (int((date_max // interval_size) + 1))

# Create intervals
df['date_interval'] = pd.cut(df['date'].astype(int), bins=range(rounded_down_min, rounded_up_max + interval_size, interval_size), right=False)

# Text Preprocessing
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess_text(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.lower() not in stop_words and token.isalpha()]
        # Apply stemming
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens
    else:
        return []

df["processed_description"] = df["subject"].apply(preprocess_text)

# Create an empty list to store dictionaries of results
result_data = []

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        # Flatten the list of lists and create a Counter
        all_words = [item for sublist in group["processed_description"].tolist() for item in sublist]
        word_counts = Counter(all_words)

        # Add data to result_data
        for word, count in word_counts.items():
            total_words = sum(word_counts.values())  # Total number of words in this time period
            tf = count / total_words  # Calculate term frequency as a fraction of total words

            # Filter DataFrame by the date interval
            start_date, end_date = name.left, name.right
            group_filtered = df[(df['date'] >= start_date) & (df['date'] < end_date)]
            group_filtered_descriptions = group_filtered["processed_description"].tolist()

            # Find occurrences of the word in the texts
            occurrences = []
            for i, text in enumerate(group_filtered_descriptions):
                if word in text:
                    occurrences.append(group_filtered.index[i])  # append the index of the full dataframe

            result_data.append({'decade': f"{start_date}-{end_date}", 'word': word, 'tf': tf, 'occurrences': occurrences})

# Create a DataFrame from the list of dictionaries
result_df = pd.DataFrame(result_data)
print(result_df)

# Export result_df to CSV
result_df.to_csv("retry_subject_tf_fraction_by_decade_with_occurrences.csv", index=False)
'''

# tfdif pages
import pandas as pd
from nltk.corpus import stopwords
import nltk
from collections import Counter
from nltk.stem import PorterStemmer
import re

df = pd.read_csv("cleaned_df.csv")
interval_size = 50

df.dropna(subset=['date'], inplace=True)

# Calculate rounded down min and rounded up max values
date_min, date_max = df['date'].min(), df['date'].max()

rounded_down_min = interval_size * (int(date_min) // interval_size)
rounded_up_max = interval_size * (int((date_max // interval_size) + 1))

# Create intervals
df['date_interval'] = pd.cut(df['date'].astype(int), bins=range(rounded_down_min, rounded_up_max + interval_size, interval_size), right=False)

# Text Preprocessing
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess_text(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.lower() not in stop_words and token.isalpha()]
        # Apply stemming
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens
    else:
        return []

df["processed_description"] = df["subject"].apply(preprocess_text)

# Create an empty list to store dictionaries of results
result_data = []

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        # Flatten the list of lists and create a Counter
        all_words = [item for sublist in group["processed_description"].tolist() for item in sublist]
        word_counts = Counter(all_words)

        # Add data to result_data
        for word, count in word_counts.items():
            total_words = sum(word_counts.values())  # Total number of words in this time period
            tf = count / total_words  # Calculate term frequency as a fraction of total words

            # Filter DataFrame by the date interval
            start_date, end_date = name.left, name.right
            group_filtered = df[(df['date'] >= start_date) & (df['date'] < end_date)]
            group_filtered_descriptions = group_filtered["processed_description"].tolist()

            # Find occurrences of the word in the texts
            occurrences = []
            for i, text in enumerate(group_filtered_descriptions):
                if word in text:
                    occurrences.append(group_filtered.index[i])  # append the index of the full dataframe

            result_data.append({'decade': f"{start_date}-{end_date}", 'word': word, 'tf': tf, 'occurrences': occurrences})

# Create a DataFrame from the list of dictionaries
result_df = pd.DataFrame(result_data)
print(result_df)

# Export result_df to CSV
result_df.to_csv("subject_tfidf_by_decade_with_occurrences.csv", index=False)
