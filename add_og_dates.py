import pandas as pd

# Read the peoples_beeswarm DataFrame
df = pd.read_csv("odnb_beeswarm.csv")

# Drop duplicate authors
df = df.drop_duplicates(subset=['cleaned_creator'], keep='first')

# Save the updated DataFrame to a new CSV file
df.to_csv("odnb_beeswarm_no_duplicates.csv", index=False)

print("Duplicates dropped and saved to peoples_beeswarm_no_duplicates.csv")
