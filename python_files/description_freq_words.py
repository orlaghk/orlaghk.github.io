"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK resources
nltk.download('stopwords')

# Load your data
df = pd.read_csv("cleaned_author_df.csv")

# Define interval size
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
        tokens = [stemmer.stem(token) for token in tokens if token.lower() not in stop_words and token.isalpha()]
        return " ".join(tokens)
    else:
        return ""

df["processed_description"] = df["description"].apply(preprocess_text)

# Calculate TF-IDF within each interval
tfidf_vectorizer = TfidfVectorizer()

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['decade', 'word', 'tfidf'])

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        tfidf_matrix = tfidf_vectorizer.fit_transform(group["processed_description"])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_values = tfidf_matrix.max(axis=0).toarray()[0]

        # Extracting decade from the interval
        decade_start = int(name.left)
        decade_end = int(name.right)
        decade = f"{decade_start}-{decade_end}"

        # Adding data to result_df using concat
        temp_df = pd.DataFrame({'decade': [decade]*len(feature_names), 'word': feature_names, 'tfidf': tfidf_values})
        result_df = pd.concat([result_df, temp_df], ignore_index=True)

# Display the result DataFrame
print(result_df)

# Export result_df to CSV
result_df.to_csv("tfidf_stemmed_by_decade.csv", index=False)
"""

"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

# Download NLTK resources
nltk.download('stopwords')

# Load your data
df = pd.read_csv("cleaned_df.csv")

# Define interval size
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
        tokens = [stemmer.stem(token) for token in tokens if token.lower() not in stop_words and token.isalpha()]
        return " ".join(tokens)
    else:
        return ""

#df["processed_description"] = df["description"].apply(preprocess_text)
df["processed_description"] = df["title"].apply(preprocess_text)

# Calculate TF within each interval
tf_vectorizer = CountVectorizer()

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['decade', 'word', 'tf'])

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        tf_matrix = tf_vectorizer.fit_transform(group["processed_description"])
        feature_names = tf_vectorizer.get_feature_names_out()
        tf_values = tf_matrix.sum(axis=0).A1  # Fix for extracting values

        # Extracting decade from the interval
        decade_start = int(name.left)
        decade_end = int(name.right)
        decade = f"{decade_start}-{decade_end}"

        # Calculate total number of words in the interval
        total_words = tf_matrix.sum()

        # Adding data to result_df as a fraction of total words
        data = {'decade': [decade] * len(feature_names),
                'word': feature_names,
                'tf': tf_values / total_words}  # TF as a fraction of total words
        result_df = pd.concat([result_df, pd.DataFrame(data)], ignore_index=True)

# Display the result DataFrame
print(result_df)

# Export result_df to CSV
result_df.to_csv("creator_tf_fraction_by_decade.csv", index=False)
"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer


# Load your data
df = pd.read_csv("cleaned_df.csv")

# Define interval size
interval_size = 50

df.dropna(subset=['date'], inplace=True)

# Calculate rounded down min and rounded up max values
date_min, date_max = df['date'].min(), df['date'].max()


rounded_down_min = interval_size * (int(date_min) // interval_size)
rounded_up_max = interval_size * (int((date_max // interval_size) + 1))

# Create intervals
df['date_interval'] = pd.cut(df['date'].astype(int), bins=range(rounded_down_min, rounded_up_max + interval_size, interval_size), right=False)

# # Text Preprocessing
# stop_words = set(stopwords.words("english"))
#stemmer = PorterStemmer()

def preprocess_text(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.lower() and token.isalpha()]
        # print(tokens)
        return " ".join(tokens)
    else:
        return ""


#df["processed_description"] = df["creator"].apply(preprocess_text)
df["processed_description"] = df["subject"].apply(preprocess_text)


# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['decade', 'word', 'tf', 'occurrences'])

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        tf_vectorizer = CountVectorizer()
        tf_matrix = tf_vectorizer.fit_transform(group["processed_description"])
        feature_names = tf_vectorizer.get_feature_names_out()
        tf_values = tf_matrix.sum(axis=0).A1  # Fix for extracting values

        # Extracting decade from the interval
        decade_start = int(name.left)
        decade_end = int(name.right)
        decade = f"{decade_start}-{decade_end}"

        # Calculate total number of words in the interval
        total_words = tf_matrix.sum()

        # Find occurrences for each word in the current decade
        occurrences = [group[group['processed_description'].str.contains(word)].index.tolist() for word in feature_names]

        # Adding data to result_df using concat
        data = {'decade': [decade] * len(feature_names),
                'word': feature_names,
                'tf': tf_values / total_words,  # TF as a fraction of total words
                'occurrences': occurrences}
        result_df = pd.concat([result_df, pd.DataFrame(data)], ignore_index=True)

# Display the result DataFrame
print(result_df)

# Export result_df to CSV
result_df.to_csv("creator_tf_fraction_by_decade_with_occurrences.csv", index=False)

av


"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK resources
nltk.download('stopwords')

# Load your data
df = pd.read_csv("cleaned_df.csv")

# Define interval size
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
        tokens = [stemmer.stem(token) for token in tokens if token.lower() not in stop_words and token.isalpha()]
        return " ".join(tokens)
    else:
        return ""

#df["processed_description"] = df["description"].apply(preprocess_text)
df["processed_description"] = df["title"].apply(preprocess_text)

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['decade', 'word', 'tfidf', 'occurrences'])

for name, group in df.groupby('date_interval'):
    # Check if the processed descriptions are not empty
    if not group["processed_description"].empty:
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(group["processed_description"])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_values = tfidf_matrix.max(axis=0).toarray()[0]

        # Extracting decade from the interval
        decade_start = int(name.left)
        decade_end = int(name.right)
        decade = f"{decade_start}-{decade_end}"

        # Find occurrences for each word in the current decade
        occurrences = [group[group['processed_description'].str.contains(word)].index.tolist() for word in feature_names]

        # Adding data to result_df using concat
        temp_df = pd.DataFrame({'decade': [decade] * len(feature_names),
                                'word': feature_names,
                                'tfidf': tfidf_values,
                                'occurrences': occurrences})
        result_df = pd.concat([result_df, temp_df], ignore_index=True)

# Display the result DataFrame
print(result_df)

# Export result_df to CSV
result_df.to_csv("title_tfidf_stemmed_by_decade_with_occurrences.csv", index=False)
"""