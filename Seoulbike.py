import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sys

# URL of the dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'

# Download the dataset
print("Downloading the dataset...")
try:
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Error downloading the file: {e}")
    sys.exit()

# Write the content to a file
with open('SeoulBikeData.csv', 'wb') as f:
    f.write(response.content)
print("File downloaded successfully.")

# Load the dataframe
try:
    df = pd.read_csv('SeoulBikeData.csv', encoding='latin1')
except FileNotFoundError:
    print("Error: SeoulBikeData.csv not found.")
    sys.exit()
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    sys.exit()

# Display the first few rows of the dataframe
print('\nOriginal DataFrame:')
print(df.head())

# --- Visualizations ---
print("\nGenerating visualizations...")

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
