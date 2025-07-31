import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataframe with 'cp949' encoding.
try:
    df = pd.read_csv('SeoulBikeData.csv', encoding='cp494')
except UnicodeDecodeError:
    df = pd.read_csv('SeoulBikeData.csv', encoding='euc-kr')


# Display the first few rows of the dataframe.
print('Original DataFrame:')
display(df.head())

# Sort the dataframe by 'Rented Bike Count'.
df_sorted = df.sort_values(by='Rented Bike Count')

# Display the sorted dataframe.
print('\nDataFrame sorted by Rented Bike Count:')
display(df_sorted.head())

# Create a histogram for 'Rented Bike Count'
plt.figure(figsize=(10, 6))
sns.histplot(df['Rented Bike Count'], bins=50, kde=True)
plt.title('Distribution of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.ylabel('Frequency')
plt.show()

# Create a box plot for 'Rented Bike Count'
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Rented Bike Count'])
plt.title('Box Plot of Rented Bike Count')
plt.xlabel('Rented Bike Count')
plt.show()

# Calculate the average 'Rented Bike Count' for each hour
average_bike_count_by_hour = df.groupby('Hour')['Rented Bike Count'].mean()

# Create a line plot of the average bike counts per hour
plt.figure(figsize=(12, 6))
sns.lineplot(x=average_bike_count_by_hour.index, y=average_bike_count_by_hour.values)
plt.title('Average Rented Bike Count by Hour')
plt.xlabel('Hour')
plt.ylabel('Average Rented Bike Count')
plt.xticks(average_bike_count_by_hour.index) # Ensure all hours are shown on the x-axis
plt.grid(True)
plt.show()

# Convert the 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Group by 'Date' and sum 'Rented Bike Count'
daily_rentals = df.groupby('Date')['Rented Bike Count'].sum()

# Create a time series plot
plt.figure(figsize=(15, 7))
daily_rentals.plot()
plt.title('Total Rented Bike Count by Date')
plt.xlabel('Date')
plt.ylabel('Total Rented Bike Count')
plt.grid(True)
plt.show()

# Create a box plot to compare 'Rented Bike Count' across different 'Seasons'
plt.figure(figsize=(10, 6))
sns.boxplot(x='Seasons', y='Rented Bike Count', data=df)

# Add titles and labels
plt.title('Rented Bike Count by Season')
plt.xlabel('Season')
plt.ylabel('Rented Bike Count')

# Display the plot
plt.show()
