import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup

# Function to search a cleaned creator on ODNB
def search_on_odnb(cleaned_creator):
    cleaned_creator = cleaned_creator.replace(" ", "+")
    
    # URL of ODNB search page
    url = f'https://www.oxforddnb.com/search?q={cleaned_creator}&searchBtn=Search&isQuickSearch=true'
    print("URL:", url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

    response = requests.get(url, headers=headers)

    # Send HTTP request
    print("Response status code:", response.status_code)
    
    # Check if request was successful
    if response.status_code == 200:
        print("searching")
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if search returned any results
        result_count = soup.select_one('span#resultTotal.count')
        if result_count:
            result_count_text = result_count.text.strip()
            # Extract numeric part of the result count string
            result_count_numeric = ''.join(filter(str.isdigit, result_count_text))
            print("Result count:", result_count_numeric)
            if int(result_count_numeric) > 0:
                return True
    elif response.status_code == 403:
        print("403 Forbidden: Access Denied")
    else:
        print("Unexpected response code:", response.status_code)
    return False

# Read the CSV file
df = pd.read_csv('finalATTEMPT.csv')

# Group by cleaned_creator and combine fields for JSON serialization
grouped_df = df.groupby('cleaned_creator').agg(lambda x: x.tolist())

# Iterate through each group
for cleaned_creator, group in grouped_df.iterrows():
    if search_on_odnb(cleaned_creator):
        print(cleaned_creator)
        # Add to CSV if found
        with open('found_on_odnb.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(group.tolist())
