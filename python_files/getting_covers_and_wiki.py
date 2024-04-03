import pandas as pd
import re
import numpy as np
import math
import ast
import requests
from bs4 import BeautifulSoup


file_path = 'diss_project/jan_work/original_df.csv'
df = pd.read_csv(file_path)


def separate_combined_words(name):
    # Split the input name into words
    words = re.findall(r'\b\w+\b', name)
    
    # Separate combined words in each word
    separated_words = []
    for word in words:
        separated_word = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)
        separated_words.append(separated_word)
    
    # Join the separated words with spaces to form the separated name
    separated_name = ' '.join(separated_words)
    return separated_name



def clean_creator_name(name):
    # Check if the value is NaN or non-string
    if pd.isna(name) or not isinstance(name, str):
        return np.nan
    
    # Extract names within parentheses using regular expression
    matches = re.findall(r'\((.*?)\)', name)
    
    if matches:
        # Extract letters outside parentheses and inside parentheses
        # Split the name by commas
        no_brack_name = re.sub(r'\(.*?\)', '', name).strip(' ,').strip()
        parts = no_brack_name.split(",")

        # Initialize initials as an empty string
        initials = ''
        if len(parts) > 2:
            # If there are more than 2 parts, extract initials from the portion after the first comma and before the second comma
            middle = parts[1]
            initials = ' '.join(word.upper() + '.' if len(word) == 1 else word.capitalize() for word in re.findall(r'\b\w+\b', middle))
        elif len(parts) == 1:
            # If there is only one part, extract initials from that part
            initials = ' '.join(word.upper() + '.' if len(word) == 1 else word.capitalize() for word in re.findall(r'\b\w+\b', parts[0]))

        outside_letters = initials
        inside_words = matches[0].split()
        inside_letters = " ".join(word.upper() + '.' if len(word) == 1 else word.capitalize() for word in inside_words)

        if outside_letters.upper() == inside_letters[:len(outside_letters)]:
            # Format as "Firstname Middlename Lastname"
            name_parts = re.split(r'[,]', name)
            lastname = name_parts[0].strip()
            first_middle_names = re.findall(r'\((.*?)\)', name)
            name = f'{lastname}, {first_middle_names}'
        else:
            # Return the original name without the content inside the parentheses or the brackets
            name = re.sub(r'\(.*?\)', '', name)
    
    # If no names within parentheses, use letters (assuming format "Lastname, Firstname Middlename")
    cleaned_name = re.sub(r'[^a-zA-Z, ]', '', name)

    parts = cleaned_name.split(',')
    
    if len(parts) == 1:
        clean = parts[0].strip()  # Only the last name is available
    elif len(parts) == 2:
        clean = f'{parts[1].strip()} {parts[0].strip()}'  # First and last name
    else:
        clean = f'{"".join(parts[1:-1]).strip()} {parts[0].strip()}'  # First, last, and middle names

    parts = clean.split(' ')
    for i in range(len(parts)):
        if len(parts[i]) == 1:
            parts[i] = f"{parts[i]}."

    # Return the modified 'clean'
    return ' '.join(parts)



    
    

def cleaned_dates(date):
    try:

        newdate = re.sub(r'\"', '', str(date))
        newdate = newdate.replace("[", "").replace("]", "").replace(".", "").replace("--","00").replace("u", "0").replace("-?", "0")

        newdate = newdate.replace("?", "0")

        if pd.isnull(newdate) or newdate == 'nan':
            return np.nan  # Return nan for 'nan' values
        
        truncated_match = re.match(r'(\d{3})-$', str(newdate))
        if truncated_match:
            return int(truncated_match.group(1) + '0')  # Complete the truncated date (e.g., "189-" becomes "1890")

        if newdate.isdigit() and len(newdate) == 4:
            return int(newdate)

        range_match = re.match(r'(\d{4})-(\d{4})', str(newdate))
        if range_match:
            start_year, end_year = int(range_match.group(1)), int(range_match.group(2))
            return int((start_year + end_year) // 2)
        

        multiple_years_match = re.findall(r'\d{4}', str(newdate))
        if multiple_years_match:
            years = list(map(int, multiple_years_match))
            return int(sum(years) // len(years))  # Calculate the mean of the years
        

        trunc_match = re.match(r'(\d{3})- - (\d{3})-$', str(date))
        if trunc_match:
            start_year, end_year = int(trunc_match.group(1) + '0'), int(trunc_match.group(2) + '0')
            return int((start_year + end_year) // 2)  # Calculate the mean of the years
        
        newdate = newdate.replace("-", "0")
        
        date_match = re.match(r'\d{1,2}/\d{1,2}/(\d{4})', str(newdate))
        if date_match:
            return int(date_match.group(1))

        c_match = re.match(r'c(\d+)', str(newdate))
        if c_match:
            return int(c_match.group(1))

        sep_match = re.match(r'[a-zA-Z]{3} (\d{2})', str(newdate))
        if sep_match:
            return int('19' + sep_match.group(1))

        year_match = re.match(r'[a-zA-Z]+ \d{1,2} (\d{4})', str(newdate))
        if year_match:
            return int(year_match.group(1))
        
        o_match = re.match(r'(\d{4}) 0 (\d{4})', str(newdate))
        if o_match:
            first_year = int(o_match.group(1))
            last_year = int(o_match.group(2))
            return int((first_year + last_year) // 2)
        
        error_match = re.match(r'l986' , str(newdate))
        if error_match:
            return int(1986)


        # If no match, return the original value
        return np.nan

    except Exception as e:
        print(f"An error occurred: {e}")
        return np.nan  # Return nan if there's an error during parsing







# Import necessary libraries
import requests
from bs4 import BeautifulSoup


# Function to get author name and occupation from Wikipedia
def get_author_info_from_wikipedia(cleaned_creator):
    if pd.isna(cleaned_creator):
        return cleaned_creator, None

    # Construct the URL for the Wikipedia page of the author
    wikipedia_url = f"https://en.wikipedia.org/wiki/{cleaned_creator.replace(' ', '_')}"

    # Send a GET request to the Wikipedia page
    response = requests.get(wikipedia_url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the occupation information in the infobox
    occupation_elements = soup.select('.infobox-data.role li')

    # Check if there are occupation items in the list
    if occupation_elements:
        # Extract the occupation from the list items
        occupations = [element.text.strip() for element in occupation_elements]
        return cleaned_creator, occupations

    # If no occupation is found, return None
    return cleaned_creator, None








def get_wikipedia_data(author_name):
    
    if isinstance(author_name, float):
        return False, 0
    
    # Construct the URL for the Wikipedia page of the author
    wikipedia_url = f"https://en.wikipedia.org/wiki/{author_name.replace(' ', '_')}"

    # Send a GET request to the Wikipedia page
    response = requests.get(wikipedia_url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the label element with specific ID and class
    label_element = soup.find('label', {'id': 'p-lang-btn-label', 'class': 'vector-dropdown-label'})

    # Check if the author has a Wikipedia page
    has_wikipedia_page = True if label_element else False

    # Extract the translation count if the author has a Wikipedia page
    translation_count = 0
    if has_wikipedia_page:
        span_element = label_element.find('span', class_='vector-dropdown-label-text')
        if span_element:
            translation_text = span_element.text.strip()
            # Extract the numeric part of the text (e.g., "127 languages" -> 127)
            try:
                translation_count = int(translation_text.split()[0])
            except (ValueError, IndexError):
                # Handle cases where translation count information is not in the expected format
                pass

    return has_wikipedia_page, translation_count


# first combine df based on creator same name and concat each column into a list
# to hold author, titles, dates, publishers, languages, subjects, descriptions
def create_df():  
    
    # Clean the 'creator' and 'date' column
    df['cleaned_creator'] = df['creator'].apply(clean_creator_name)
    df['date'] = df['date'].apply(cleaned_dates)     
    df = df.dropna(subset=['cleaned_creator'])

    # Combine rows based on the 'creator' column and concatenate other columns into lists
    combined_df = df.groupby('cleaned_creator').agg(lambda x: x.tolist()).reset_index()

    # Create a new DataFrame with separated lists
    new_df = pd.DataFrame({
        'author': combined_df['cleaned_creator'],
        'creator': combined_df['creator'],
        'titles': combined_df['title'],
        'dates': combined_df['date'],
        'publishers': combined_df['publisher'],
        'languages': combined_df['language'],
        'subjects': combined_df['subject'],
        'descriptions': combined_df['description']
    })

    print(len(new_df))

    # Save the new DataFrame to a CSV file
    new_df.to_csv('combined_data.csv', index=False)


file_path = 'diss_project/jan_work/combined_data.csv'
new_df = pd.read_csv(file_path)
     
# then check if has occupation and print them.  

import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def preprocess_occupations(occupations):
    # Initialize Porter Stemmer
    stemmer = PorterStemmer()
    synonym_mapping = {
    'write': ['write', 'author', 'wordsmith', 'scribe', 'writer', 'penman', 'journalist', 'playwright', 'screenwriter',],
    'novel': ['novel', 'novelist', 'fictionist', 'storyteller', 'illustrator'],
    'poet': ['poet', 'bard', 'versifier', 'rhymester'],
    'editor': ['editor', 'redactor', 'reviser', 'copyeditor'],
    'researcher': ['researcher', 'scholar', 'academic', 'historian'],
    'publisher': ['publisher', 'manuscript curator', 'bibliophile'],
    'language': ['linguist', 'lexicographer', 'grammarian', 'etymologist'],
    # Add more categories and synonyms as needed
    }   
    def preprocess_single_occupation(occupation):
        occupation = occupation.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(occupation.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        for category, synonyms in synonym_mapping.items():
            if any(synonym in stemmed_tokens for synonym in synonyms):
                return True
        return False

    any_match = any(preprocess_single_occupation(occupation) for occupation in occupations)
    print(f"Occupations: {occupations}")
    return any_match

# occupations = ["Author", "Novelist", "Poet", "Editor", "Journalist", "Historian", "Lexicographer"]
# result = preprocess_occupations(occupations)
# print(f"Match: {result}")

for index, row in new_df.head(100).iterrows():

    creator_name, occupations = get_author_info_from_wikipedia(row['author'])

    if occupations is not None:
        result = preprocess_occupations(occupations)

        if result:
            # If the result is True, add the row to a new CSV
            row.to_csv('authors_only.csv', mode='a', header=not pd.read_csv('authors_only.csv').shape[0])  # Append row to CSV

        elif result is False:
            print(f"Creator Name: {row['creator']}")
            
            # Ask the user for confirmation to add the row
            user_input = input("Do you want to add this row? (yes/no): ")
            if user_input.lower() == 'yes':
                row.to_csv('authors_only.csv', mode='a', header=not pd.read_csv('authors_only.csv').shape[0])  # Append row to CSV
                print("Row added.")
            else:
                print("Row not added.") 

import os
import pandas as pd


new_df = new_df.iloc[55000:]

csv_file_path = '/afs/inf.ed.ac.uk/user/s20/s2084384/Desktop/diss-proj/diss_project/jan_work/authors_only.csv'
#csv_file_path ='/Users/orlagh/Documents/4thYear/project/working-code/jan_work/authors_only.csv'
# Create an empty CSV file with a header
header = new_df.columns.tolist()

# Counter to track the row index
row_counter = 0

# Iterate through the first n rows of the DataFrame
for index, row in new_df.iterrows():
    row_counter += 1

    creator_name, occupations = get_author_info_from_wikipedia(row['author'])

    if occupations is not None:
        result = preprocess_occupations(occupations)

        if result:
            # Create a DataFrame with the current row and the same columns as the first row
            current_row_df = pd.DataFrame([row.values], columns=header)
            # Append the row to the CSV
            current_row_df.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)
            print(f"Row {row_counter} added.")

        elif result is False:
            print(f"Creator Name: {row['creator']}")
            
            # Ask the user for confirmation to add the row
            user_input = input("Do you want to add this row? (yes/no): ")
            if user_input.lower() == 'yes':
                # Create a DataFrame with the current row and the same columns as the first row
                current_row_df = pd.DataFrame([row.values], columns=header)
                # Append the row to the CSV
                current_row_df.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)
                print(f"Row {row_counter} added.")
            else:
                print(f"Row {row_counter} not added.")
