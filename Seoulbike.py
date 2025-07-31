import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# URL of the dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'

# Download the dataset
print("Downloading the dataset...")
response = requests.get(url)

if response.status_code == 200:
    with open('SeoulBikeData.csv', 'wb') as f:
        f.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
    exit() # Exit the script if file download fails

# Load the dataframe
try:
    df = pd.read_csv('SeoulBikeData.csv', encoding='latin1')
except FileNotFoundError:
    print("CSV file not found. Please ensure the download was successful.")
    exit()

# Display the first few rows of the dataframe
print('\nOriginal DataFrame:')
print(df.head())

# Sort the dataframe by 'Rented Bike Count'
df_sorted = df.sort_values(by='Rented Bike Count')

# Display the sorted dataframe
print('\nDataFrame sorted by Rented Bike Count:')
print(df_sorted.head())

# --- Visualizations ---
print("\nStarting visualizations...")

# Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Rented Bike Count'], bins=50, kde=True)
plt.title('Distribution of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.ylabel('Frequency')
plt.show()

# Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Rented Bike Count'])
plt.title('Box Plot of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.show()

# Average Rented Bike Count by Hour
average_bike_count_by_hour = df.groupby('Hour')['Rented Bike Count'].mean()

plt.figure(figsize=(12, 6))
sns.lineplot(x=average_bike_count_by_hour.index, y=average_bike_count_by_hour.values)
plt.title('Average Rented Bike Count by Hour')
plt.xlabel('Hour')
plt.ylabel('Average Rented Bike Count')
plt.xticks(average_bike_count_by_hour.index)
plt.grid(True)
plt.show()

# Total Rented Bike Count by Date
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
daily_rentals = df.groupby('Date')['Rented Bike Count'].sum()

plt.figure(figsize=(15, 7))
daily_rentals.plot()
plt.title('Total Rented Bike Count by Date')
plt.xlabel('Date')
plt.ylabel('Total Rented Bike Count')
plt.grid(True)
plt.show()

# Rented Bike Count by Season
plt.figure(figsize=(10, 6))
sns.boxplot(x='Seasons', y='Rented Bike Count', data=df)
plt.title('Rented Bike Count by Season')
plt.xlabel('Season')
plt.ylabel('Rented Bike Count')
plt.show()

print("\nAll tasks completed.")
