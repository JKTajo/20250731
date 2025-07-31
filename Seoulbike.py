# -------------------------------------------
# 🔧 설치: 최초 1회만
# -------------------------------------------
!pip install kagglehub[pandas-datasets]
!apt-get -qq install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf

# -------------------------------------------
# 📁 데이터 다운로드
# -------------------------------------------
import kagglehub
import os

dataset_path = kagglehub.dataset_download("saurabhshahane/seoul-bike-sharing-demand-prediction")
print("📦 다운로드 경로:", dataset_path)

# -------------------------------------------
# 📊 데이터 불러오기
# -------------------------------------------
import pandas as pd

csv_file = None
for file in os.listdir(dataset_path):
    if file.endswith(".csv"):
        csv_file = os.path.join(dataset_path, file)
        break

df = pd.read_csv(csv_file)
df.head()

# -------------------------------------------
# 🎨 한글 폰트 설정
# -------------------------------------------
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'
plt.plot(df['Rented Bike Count'][:50])
plt.title('자전거 대여 수요')
plt.xlabel('시간')
plt.ylabel('대여 수')
plt.grid(True)
plt.show()

# -------------------------------------------
# 💾 streamlit 코드 저장
# -------------------------------------------
streamlit_code = """
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

# Step 1: 다운로드
path = kagglehub.dataset_download("saurabhshahane/seoul-bike-sharing-demand-prediction")

# Step 2: CSV 찾기
csv_file = None
for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_file = os.path.join(path, file)
        break

if not csv_file:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.stop()

# Step 3: 읽기
df = pd.read_csv(csv_file)

# 사이드바
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("KaggleHub 기반 Streamlit 앱")
st.sidebar.markdown(\"\"\"
이 앱은 서울시 자전거 대여 수요 데이터를 기반으로 한 시각화 도구입니다.
데이터를 탐색하고 원하는 인덱스를 선택하여 분석할 수 있습니다.
\"\"\")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터 보기", "🔍 인덱스별 분석"])

# Tab 1
with tab1:
    st.header("📌 데이터 요약")
    st.dataframe(df.head())
    st.dataframe(df.describe())

# Tab 2
with tab2:
    st.header("📊 전체 데이터 보기")
    st.dataframe(df)

# Tab 3
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    # 정렬
    sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
    ascending = st.radio("정렬 방식", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    # 히스토그램
    if "Rented Bike Count" in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(sorted_df["Rented Bike Count"], bins=30, kde=True, ax=ax)
        st.pyplot(fig)

    # 다중 인덱스
    selected_indices = st.multiselect(
        "인덱스를 선택하세요",
        options=list(sorted_df.index),
        default=[0]
    )

    if selected_indices:
        st.dataframe(sorted_df.loc[selected_indices])
    else:
        st.info("인덱스를 하나 이상 선택해주세요.")
"""

# py 파일로 저장
with open("Seoulbike_app.py", "w") as f:
    f.write(streamlit_code)

print("✅ Streamlit 코드가 Seoulbike_app.py로 저장되었습니다.")
