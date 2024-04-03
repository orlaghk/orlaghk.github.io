import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
tree = ET.parse('BIBLIOGRAPHIC_11573881650004341_1.xml')
root = tree.getroot()

# # Create an empty list to store data
# data = []

# # Extract data from XML where 'Type' category has the value 'text' and append to the list
# for description in root.findall('.//rdf:Description', namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'dc': 'http://purl.org/dc/elements/1.1/'}):
#     if description.find('{http://purl.org/dc/elements/1.1/}type', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}) is not None:
#         row = {}
#         for child in description:
#             # Extract local name of the element (without namespace prefix)
#             column_name = child.tag.split('}')[1]
#             # Store the data in the dictionary
#             if 'text' in str(child.text):
#                 row[column_name] = child.text
#         data.append(row)

# # Create a DataFrame from the list of dictionaries
# df = pd.DataFrame(data)

file_path = 'author_df.csv'
df = pd.read_csv(file_path)

print(len(df))

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup



author_df_500 = df.head(500).copy()
author_df_500['another_url'] = ''

# Function to search for images based on the title
def search_image(title, creator, publisher):
    search_query = f'{title} written by {creator} published by {publisher}'
    search_query = search_query.replace(' ', '+')  # Replace spaces with '+' for the URL

    search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'

    #search_url = f'https://www.google.com/search?q={title}&tbm=isch'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags]
    print(len(img_urls))
    return img_urls[1] if len(img_urls) > 1 else None

# Create an empty list to store image URLs
images_urls = []



# Iterate through DataFrame rows and search for images based on titles
for index, row in tqdm(author_df_500.iterrows(), total=len(author_df_500), desc="Searching Images"):
    image_url = search_image(row['title'], row['creator'], row['publisher'])
    if image_url:
        images_urls.append(image_url)
    else:
        images_urls.append(None) 

author_df_500['url'] = images_urls

author_df_500.to_csv('author_df_500.csv', index=False)


