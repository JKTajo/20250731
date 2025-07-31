import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Install a Korean font
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

# Set the font to a Korean font
plt.rc('font', family='NanumBarunGothic')

# URL of the dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a file
    with open('SeoulBikeData.csv', 'wb') as f:
        f.write(response.content)
    print("파일이 성공적으로 다운로드되었습니다.")
else:
    print(f"파일 다운로드 실패. 상태 코드: {response.status_code}")

# Load the dataframe
df = pd.read_csv('SeoulBikeData.csv', encoding='latin1')

# Display the first few rows of the dataframe
print('원본 데이터프레임:')
display(df.head())

# Sort the dataframe by 'Rented Bike Count'
df_sorted = df.sort_values(by='Rented Bike Count')

# Display the sorted dataframe
print('\n대여된 자전거 수로 정렬된 데이터프레임:')
display(df_sorted.head())

# Create a histogram for 'Rented Bike Count'
plt.figure(figsize=(10, 6))
sns.histplot(df['Rented Bike Count'], bins=50, kde=True)
plt.title('대여된 자전거 수의 분포')
plt.xlabel('대여된 자전거 수')
plt.ylabel('빈도')
plt.show()

# Create a box plot for 'Rented Bike Count'
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Rented Bike Count'])
plt.title('대여된 자전거 수의 상자 그림')
plt.xlabel('대여된 자전거 수')
plt.show()

# Calculate the average 'Rented Bike Count' for each hour
average_bike_count_by_hour = df.groupby('Hour')['Rented Bike Count'].mean()

# Create a line plot of the average bike counts per hour
plt.figure(figsize=(12, 6))
sns.lineplot(x=average_bike_count_by_hour.index, y=average_bike_count_by_hour.values)
plt.title('시간대별 평균 대여 자전거 수')
plt.xlabel('시간')
plt.ylabel('평균 대여 자전거 수')
plt.xticks(average_bike_count_by_hour.index)
plt.grid(True)
plt.show()

# Convert the 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Group by 'Date' and sum 'Rented Bike Count'
daily_rentals = df.groupby('Date')['Rented Bike Count'].sum()

# Create a time series plot
plt.figure(figsize=(15, 7))
daily_rentals.plot()
plt.title('날짜별 총 대여 자전거 수')
plt.xlabel('날짜')
plt.ylabel('총 대여 자전거 수')
plt.grid(True)
plt.show()

# Create a box plot to compare 'Rented Bike Count' across different 'Seasons'
plt.figure(figsize=(10, 6))
sns.boxplot(x='Seasons', y='Rented Bike Count', data=df)
plt.title('계절별 대여 자전거 수')
plt.xlabel('계절')
plt.ylabel('대여 자전거 수')
plt.show()
