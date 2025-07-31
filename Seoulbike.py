import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sys

# --- Step 1: Download the data ---
print("Attempting to download the dataset...")
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("CRITICAL ERROR: Could not download the file. Please check your internet connection.")
    print(f"Details: {e}")
    sys.exit()

with open('SeoulBikeData.csv', 'wb') as f:
    f.write(response.content)
print("Dataset downloaded successfully.")

# --- Step 2: Load the data into a DataFrame ---
print("\nLoading data into pandas DataFrame...")
try:
    df = pd.read_csv('SeoulBikeData.csv', encoding='latin1')
except FileNotFoundError:
    print("CRITICAL ERROR: 'SeoulBikeData.csv' not found. The script will exit.")
    sys.exit()
except Exception as e:
    print(f"CRITICAL ERROR: Failed to read the CSV file. Details: {e}")
    sys.exit()

print("Data loaded successfully. Here is a preview:")
print(df.head())

# --- Step 3: Create visualizations ---
print("\nGenerating visualizations...")

# Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Rented Bike Count'], bins=50, kde=True)
plt.title('Distribution of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Rented Bike Count'])
plt.title('Box Plot of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.grid(True)
plt.show()

print("\nScript has finished all tasks.")
