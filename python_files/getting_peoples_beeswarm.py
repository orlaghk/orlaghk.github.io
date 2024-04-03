'''import numpy as np
import ast
import pandas as pd

data = pd.read_csv('/Users/orlagh/Documents/4thYear/project/working-code/jan_work/beeswarm_df_copy.csv')


def fix_format1(entry):
    if isinstance(entry, str):
        entry = entry.replace('""', '"').replace("''", "'")
        if '""' in entry or "''" in entry:
            print(entry)
def format_entry(entry):
    if isinstance(entry, str):
        if entry.startswith('"['):
            # Removing leading and trailing square brackets
            entry = entry[1:-1]
            # Replacing double quotes with single quotes
            entry = entry.replace('"', "'")
            # Replacing square brackets with parentheses
            entry = entry.replace('[', '(')
            entry = entry.replace(']', ')')
        elif entry.startswith('['):
            # Removing leading and trailing square brackets
            entry = entry[2:-2]
            # Replacing double quotes with single quotes
            entry = entry.replace('"', "'")
            # Replacing square brackets with parentheses
            entry = entry.replace('[', '(')
            entry = entry.replace(']', ')')
        elif entry.startswith("'["):
            # Removing leading and trailing single quotes
            entry = entry[2:-2]
            # Replacing double quotes with single quotes
            entry = entry.replace('"', "'")
            # Replacing square brackets with parentheses
            entry = entry.replace('[', '(')
            entry = entry.replace(']', ')')
            # Reformatting entire string with "[ ]"
            entry = f"[{entry}]"
        else:
            # Replacing double quotes with single quotes
            entry = entry.replace('"', "'")
        
        # Replacing 'nan' or ', nan,' with 'Not available.'
        if 'nan' in entry or ", 'nan'," in entry:
            entry = entry.replace('nan', 'Not available.')
            entry = entry.replace(", 'Not available',", ", 'Not available.',")
            entry = entry.replace(",'nan',", ",'Not available.',")
            entry = entry.replace("nan,", "Not available.,")
    return entry

def fix_format(entry):
    if isinstance(entry, str):
        entry = entry.replace('""', '"').replace("''", "'")
        
        # Check for double brackets and remove them
        if entry.startswith('"[') or entry.startswith("'["):
            entry = entry[2:-2]
        elif entry.startswith('['):
            entry = entry[1:-1]
        
        # Replacing double quotes with single quotes
        entry = entry.replace('"', "'")
    
        # Replacing 'nan' or ', nan,' with 'Not available.'
        if 'nan,' in entry or ', nan' in entry or ", 'nan'" or "'nan' ," in entry or "[nan" in entry or "nan]" in entry :
            entry = entry.replace('nan', 'Not available.')
            entry = entry.replace(", 'Not available',", ", 'Not available.',")
            entry = entry.replace(",'nan',", ",'Not available.',")
            entry = entry.replace("nan,", "Not available.,")
            
        entry = f'"[{entry}]"'
    return entry


# Identify columns that contain string representations of lists
list_columns = data.applymap(lambda x: isinstance(x, str) and x.startswith('"[') and x.endswith(']"')).any()

# Fix the format for each entry in the identified columns
for column in list_columns[list_columns].index:
    data[column] = data[column].apply(fix_format)

# Print fixed data
print(data['titles'])

data.to_csv('maybe_beeswarm.csv', index=False)
'''


''
import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import ast

data = pd.read_csv('/Users/orlagh/Documents/4thYear/project/working-code/maybe_beeswarm.csv')

def search_image(titles, creators):
    urls = []
    c=0
    print(titles)
    for title in titles:
        print(title)
        creator = creators[c]  # Get the corresponding creator for the current title
        search_query = f'book cover of {title} written by {creator}'
        search_query = search_query.replace(' ', '+')  # Replace spaces with '+' for the URL

        search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'

        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = [img['src'] for img in img_tags]

        if len(img_urls) > 1:
            urls.append(img_urls[1])
        else:
            urls.append('https://www.uoduckstore.com/TDS%20Product%20Images/QuickStudy%20Book%20for%20Calculus_1.jpg?resizeid=3&resizeh=195&resizew=195')
        c +=1
    return urls
'''
# Create an empty list to store image URLs
images_urls = []

# Iterate through DataFrame rows and search for images based on titles
for index, row in tqdm(data.iterrows(), total=len(data), desc="Searching Images"):
    # Convert the string representation of the list to a list of titles
    titles = ast.literal_eval(row['titles'])
    image_url = search_image(titles, ast.literal_eval(row['creator']))
    images_urls.append(image_url)

data['urls'] = images_urls

# Save the DataFrame to a CSV file
data.to_csv('z.csv', index=False)



data = pd.read_csv('/Users/orlagh/Documents/4thYear/project/working-code/people.csv')'''


def search_image(titles, creators):
    urls = []
    for title, creator in zip(titles, creators):  # Iterate over titles and creators simultaneously
        search_query = f'book cover of {title} written by {creator}'
        print(search_query)
        search_query = search_query.replace(' ', '+')  # Replace spaces with '+' for the URL

        search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'

        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = [img['src'] for img in img_tags]

        if len(img_urls) > 1:
            url = img_urls[1]
        else:
            url = 'https://www.uoduckstore.com/TDS%20Product%20Images/QuickStudy%20Book%20for%20Calculus_1.jpg?resizeid=3&resizeh=195&resizew=195'
        urls.append(url)

    return urls
all_urls = []
#  Iterate through DataFrame rows and search for images based on titles
for index, row in tqdm(data.iterrows(), total=len(data), desc="Searching Images"):
    # Convert the string representation of the list to a list of titles
    author = row['author']
    titles = row['titles'].strip("[]").split("', '")
    creators = ast.literal_eval(row['creator'])
    print(titles, creators)
    image_urls = search_image(titles, creators)
    all_urls.append(image_urls)

# Assign the list of lists to the 'urls' column of the DataFrame
data['urls'] = all_urls

# Save the DataFrame to a CSV file
data.to_csv('beeswarm_people.csv', index=False)



import csv
import re

# getting all the files that have life span in creator
import pycountry

def is_country(word):
    try:
        country = pycountry.countries.lookup(word)
        return True
    except LookupError:
        return False

def contains_country(creator):
    words = creator.split()
    for word in words:
        if is_country(word):
            print(word)
            return True
    return False

def contains_undesired_location(creator):
    undesired_locations = ["European Coal and Steel CommunityTreaties", 
                           "United Provinces of the Netherlands",
                           "Great Britain", 
                           "Spain", 
                           "United States", 
                           "England and Wales",
                           "France",
                           "Holy Roman Empire",
                           "Netherlands",
                           "Denmark"]
    for location in undesired_locations:
        if location in creator:
            print(creator)
            return True
    return False

def check_creator_column(filename):
    # Open the CSV file
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        matching_rows = []
        
        # Iterate over rows and check the 'creator' column
        for row in reader:
            creators = row['creator']
            # Check if the creator column contains any of the specified formats
            if any(re.match(r'\d{4}-\d{0,4}', creator.strip()) for creator in creators.split(",")):
                # Check if any country is present in the creator column
                if contains_undesired_location(creators):
                    include_row = input(f"Include this row? {row}. Enter 'yes' or 'no': ").strip().lower()
            
                    if include_row == 'y':
                        matching_rows.append(row)
                    elif include_row == 'n':
                        continue
                    else:
                        print("Invalid input. Skipping this row.")
                else:
                    matching_rows.append(row)
        
        # Write matching rows to the new CSV file
        if matching_rows:
            with open('creator_person.csv', mode='w', newline='', encoding='utf-8') as output_file:
                fieldnames = matching_rows[0].keys()
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(matching_rows)
                
            print("Matching rows have been written to creator_person.csv")
                
check_creator_column('combined_data.csv')

# creating people_df




def combine_csv(modified_author_file, creator_person_file, output_file):
    # Read modified_author.csv and store its contents in a set to keep track of unique rows
    modified_author_set = set()
    with open(modified_author_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip the index column
            modified_author_set.add((row['author'], row['creator'], row['titles'], row['dates'], row['publishers'], row['languages'], row['subjects'], row['descriptions']))
    
    # Open creator_person.csv and append rows that are not duplicates to the set
    with open(creator_person_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row['author'], row['creator'], row['titles'], row['dates'], row['publishers'], row['languages'], row['subjects'], row['descriptions']) not in modified_author_set:
                modified_author_set.add((row['author'], row['creator'], row['titles'], row['dates'], row['publishers'], row['languages'], row['subjects'], row['descriptions']))
    
    # Write the combined unique rows to the output file
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['author', 'creator', 'titles', 'dates', 'publishers', 'languages', 'subjects', 'descriptions'])
        writer.writerows(modified_author_set)

combine_csv('modified_author.csv', 'creator_person.csv', 'combined_output.csv')
