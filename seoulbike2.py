import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

# ✅ Mac 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# ✅ KaggleHub로 데이터 다운로드
path = kagglehub.dataset_download("saurabhshahane/seoul-bike-sharing-demand-prediction")

# ✅ CSV 파일 경로 찾기
csv_file = None
for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_file = os.path.join(path, file)
        break

if not csv_file:
    st.error("❌ CSV 파일을 찾을 수 없습니다.")
    st.stop()

# ✅ 데이터 불러오기
df = pd.read_csv(csv_file)

# ✅ 사이드바
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("KaggleHub 기반 Streamlit 앱")
st.sidebar.markdown("""
서울시 자전거 대여 수요 데이터를 시각화하고,  
정렬 및 인덱스 선택 기능을 통해 분석할 수 있습니다.
""")

# ✅ 탭 구성
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터", "🔍 인덱스 분석"])

# 📌 Tab 1
with tab1:
    st.header("📌 데이터 요약")
    st.dataframe(df.head())
    st.dataframe(df.describe())

# 📊 Tab 2
with tab2:
    st.header("📊 전체 데이터")
    st.dataframe(df)

# 🔍 Tab 3
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    # 정렬 옵션
    sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
    ascending = st.radio("정렬 방식", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    # 그래프 표시
    if "Rented Bike Count" in df.columns:
        st.subheader("🎯 대여량 분포")
        fig, ax = plt.subplots()
        sns.histplot(sorted_df["Rented Bike Count"], bins=30, kde=True, ax=ax)
        ax.set_title("자전거 대여량 히스토그램")
        ax.set_xlabel("대여 수")
        ax.set_ylabel("빈도")
        st.pyplot(fig)
    else:
        st.warning("⚠️ 'Rented Bike Count' 컬럼이 없어 히스토그램을 그릴 수 없습니다.")

    # 인덱스 선택
    st.subheader("📌 원하는 인덱스 선택")
    selected_indices = st.multiselect(
        "데이터 인덱스를 선택하세요",
        options=list(sorted_df.index),
        default=[0]
    )

    if selected_indices:
        st.dataframe(sorted_df.loc[selected_indices])
    else:
        st.info("인덱스를 하나 이상 선택해주세요.")
