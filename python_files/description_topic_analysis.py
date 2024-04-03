
import pandas as pd
import nltk
from nltk.corpus import stopwords
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load your data
df = pd.read_csv("cleaned_author_df.csv")

# Text Preprocessing for LDA
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.lower() not in stop_words and token.isalpha()]
        return tokens
    else:
        return []

df["processed_description"] = df["description"].apply(preprocess_text)

# Perform LDA Analysis
text_data = df['processed_description'].tolist()

# Create a dictionary
dictionary = Dictionary(text_data)

# Create a bag-of-words corpus
corpus = [dictionary.doc2bow(doc) for doc in text_data]

coherence_methods = "c_uci", "u_mass", "c_v"

# Function to train LDA model and print top words
def train_lda_and_print_top_words(num_topics, num_passes):
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=num_passes)
    coherence_model = CoherenceModel(model=lda_model, texts=text_data, dictionary=dictionary, coherence='c_uci')

    coherence_score = coherence_model.get_coherence()
    
    print(f'\nNum Topics: {num_topics}, Coherence Score: {coherence_score}')

    # Print the top words for each topic
    for i, topic in lda_model.print_topics(num_topics=num_topics, num_words=10):
        print(f"Topic #{i + 1}: {topic}")

if __name__ == '__main__':
    # Run LDA 3 times with 19 topics each
    for _ in range(3):
        train_lda_and_print_top_words(num_topics=19, num_passes=10)
