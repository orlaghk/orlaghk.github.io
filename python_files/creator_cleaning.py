import pandas as pd
import re
import numpy as np
import math
import ast

# Load the CSV file into a DataFrame
file_path = 'original_df.csv'
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

def remove_unwanted_words(text):
    # Words to remove from the creator
    words_to_remove = ["active", "afterwards", "approximately", "former owner", "formerly"]
    # Titles to remove
    titles_to_remove = [
    "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.",
    "Hon.", "Rev.", "Capt.", "Sgt.",
    "Sir", "Dame", "Lady",
    "Esq.",
    "Ph.D.", "M.D.",
    "Jr.", "Sr.", "II", "III",
    "Count", "Countess", "Baron", "Baroness",
    "Prince", "Princess", "King", "Queen",
    "Governor", "Mayor", "Senator"]

    # Create a regular expression pattern to match the words and titles to remove
    pattern = r'\b(?:' + '|'.join(map(re.escape, words_to_remove + titles_to_remove)) + r')\b'

    # Remove the matched words and titles from the text using regular expressions
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()

    return cleaned_text

def clean_creator_name(name):
    # Check if the value is NaN or non-string
    if pd.isna(name) or not isinstance(name, str):
        return np.nan
    
    name = remove_unwanted_words(name)
    
    # Extract names within parentheses using regular expression
    matches = re.findall(r'\((.*?)\)', name)
    
    if matches:
        # Extract letters outside parentheses and inside parentheses
        # Split the name by commas
        no_brack_name = re.sub(r'\(.*?\)', '', name).strip(' ,')
        parts = no_brack_name.split(",")

        
        # Initialize initials as an empty string
        initials = ''
        if len(parts) > 2:
            # If there are more than 2 parts, extract initials from the portion after the first comma and before the second comma
            middle = parts[1]
            initials = ''.join(word[0].upper() for word in re.findall(r'\b\w+\b', middle) if word.isalpha())
        elif len(parts) == 1:
            # If there is only one part, extract initials from that part
            initials = ''.join(word[0].upper() for word in re.findall(r'\b\w+\b', parts[0]) if word.isalpha())

        outside_letters = initials
        inside_words = matches[0].split()
        inside_letters = "".join(word[0] for word in inside_words).upper()


        if outside_letters.upper() == inside_letters[:len(outside_letters)]:
            # Format as "Firstname Middlename Lastname"
            name_parts = re.split(r'[,.]', name)
            lastname = name_parts[0].strip()
            first_middle_names = re.findall(r'\((.*?)\)', name)
            name = f'{lastname},{first_middle_names}'
        else:
            # Return the original name without the content inside the parentheses or the brackets
            name = re.sub(r'\(.*?\)', '', name)
            #print("not match", name)
    
    
    
    # If no names within parentheses, use letters (assuming format "Lastname, Firstname Middlename")
    cleaned_name = re.sub(r'[^a-zA-Z, ]', '', name)
    parts = cleaned_name.split(',')
    if len(parts) == 1:
        clean =  parts[0].strip()  # Only the last name is available
    elif len(parts) == 2:
        clean = f'{parts[1].strip()} {parts[0].strip()}'  # First and last name
    else:
        clean = f'{"".join(parts[1:-1]).strip()} {parts[0].strip()}'  # First, last, and middle names

       
    return separate_combined_words(clean) 

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

def clean_titles(title_str):
    print(title_str)
    try:
        # Check if the value is NaN
        if pd.isna(title_str):
            return []  # Return an empty list for NaN values
        
        # Evaluate the string representation of the list and replace 'nan' with actual NaN values
        titles_list = eval(str(title_str).replace('nan', 'math.nan'))
    except (SyntaxError, NameError):
        # Handle the case where the string cannot be evaluated properly
        titles_list = []
    print(titles_list)
    return titles_list



# Clean the 'creator' and 'date' column
df['creator'] = df['creator'].apply(clean_creator_name)
df['date'] = df['date'].apply(cleaned_dates)
#df['title'] = df['title'].apply(clean_titles)



# Save DataFrames to CSV files
df.to_csv('cleaned_author_df.csv', index=False)

