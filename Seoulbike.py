import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sys

# This is a pure Python script. It does not contain any terminal commands.

# --- Step 1: Download the data ---
print("Attempting to download the dataset...")
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'

try:
    response = requests.get(url)
    # Check if the download was successful
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"CRITICAL ERROR: Could not download the file. Please check your internet connection.")
    print(f"Details: {e}")
    sys.exit() # Exit the script because it cannot continue without the data

# Save the downloaded data to a file
with open('SeoulBikeData.csv', 'wb') as f:
    f.write(response.content)
print("Dataset downloaded successfully.")


# --- Step 2: Load the data into a DataFrame ---
print("\nLoading data into pandas DataFrame...")
try:
    # We use 'latin1' encoding because it is robust and works for this file.
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
