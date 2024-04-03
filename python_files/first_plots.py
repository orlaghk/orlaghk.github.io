import pandas as pd
import ast

file_path = 'famous_frequent/famous_frequent_df.csv'
df = pd.read_csv(file_path)

df = df[df['translation_count'] !=0]

print("length of df with translation count over 0:", len(df))
print("length of df with translation count over 1:", len(df[df['translation_count'] > 1]))
print("length of df with translation count = 2:", len(df[df['Frequency'] == 2]))
print("length of df with translation count over 5:", len(df[df['Frequency'] > 5]))

# Function to find earliest and latest year in a list of years
def find_earliest_latest_years(years_list_str):
    years_list = ast.literal_eval(years_list_str)  # Convert string to list
    earliest_year = min(years_list)
    latest_year = max(years_list)
    return earliest_year, latest_year

# Apply the function to 'Years' column and store the results in new columns
df[['earliest_year', 'latest_year']] = df['Years'].apply(find_earliest_latest_years).apply(pd.Series)

df.drop(columns=['Years'], inplace=True)
df.drop(columns=['Titles'], inplace=True)
df.drop(columns=['has_wikipedia_page'], inplace=True)


# sorted by most famous
df = df.sort_values(by='translation_count', ascending=False) 

print(df['Frequency'].max())
print(df['Frequency'].min())

# Define the bins for categorization
bins = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]

# Define labels for each category
labels = ['0-14', '15-29', '30-44', '45-59', '60-74', '75-89', '90-104', '105-119', '120-134', '135-149', '150-164', '165-179', '180-194', '195-210']


# Create the 'frequency_categories' column using pd.cut()
df['frequency_categories'] = pd.cut(df['Frequency'], bins=bins, labels=labels, right=False)

print("length of top famous and frequent :" , len(df))


df.head(200).to_csv('famous_frequent/top_famous_gantt.csv',index=False)


# # sorted by more frequence
# df = df.sort_values(by='Frequency', ascending=False)

# df.head(200).to_csv('famous_frequent/top_frequent_gantt.csv',index=False)

# df = df.head(20)
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime
# # Convert date columns to datetime objects
# df['earliest_year'] = pd.to_datetime(df['earliest_year'])
# df['latest_year'] = pd.to_datetime(df['latest_year'])

# # Calculate the duration of each task
# df['duration'] = (df['latest_year'] - df['earliest_year'] )/ pd.Timedelta(days=365.25)

# # Create a figure and axis
# fig, ax = plt.subplots(figsize=(10, 6))


# # Plot Gantt chart
# for i, row in df.iterrows():
#     creator = row['Creator']
#     start_date = mdates.date2num(row['earliest_year'])
#     end_date = mdates.date2num(row['latest_year'])
    
#     # Assign different colors based on frequency categories
#     color = 'C{}'.format(i % 10)  # Use different colors for each creator
    
#     ax.barh(creator, end_date - start_date, left=start_date, color=color, label=creator)

# # Beautify the plot
# ax.xaxis_date()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax.yaxis.set_visible(False)
# plt.xlabel('Date')
# plt.title('Gantt Chart of Creators')

# ax.set_xlim(df['earliest_year'].min(), df['latest_year'].max())


# # Add a legend
# plt.legend()

# # Show the plot
# plt.show()

