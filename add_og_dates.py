import pandas as pd

# Read the peoples_beeswarm DataFrame
df = pd.read_csv("peoples_beeswarm.csv")

# Function to add space before each capital letter in the middle of a word
def add_space_before_mid_word_capital(s):
    new_string = ''
    for i in range(len(s) - 1):
        if s[i].islower() and s[i+1].isupper():
            new_string += s[i] + ' '
        else:
            new_string += s[i]
    new_string += s[-1]  # Adding the last character
    return new_string

# Apply the function to the 'cleaned_creator' column
df['author'] = df['author'].apply(add_space_before_mid_word_capital)

# Save the updated DataFrame to a new CSV file
df.to_csv("peoples_beeswarm_with_spaces.csv", index=False)
