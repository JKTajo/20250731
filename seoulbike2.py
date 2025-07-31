import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ 한글 폰트 설정 (Mac 전용)
plt.rcParams['font.family'] = 'AppleGothic'

# ✅ CSV 파일 로드 (GitHub에 함께 업로드한 경우)
DATA_PATH = "SeoulBikeData.csv"

if not os.path.exists(DATA_PATH):
    st.error("❌ 'SeoulBikeData.csv' 파일이 존재하지 않습니다.")
    st.stop()

df = pd.read_csv(DATA_PATH, encoding='ISO-8859-1')

# ✅ 사이드바
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("GitHub 기반 Streamlit 앱")
st.sidebar.markdown("""
이 앱은 서울시 자전거 대여 수요 데이터를 기반으로 한 시각화 도구입니다.  
데이터를 탐색하고 원하는 인덱스를 선택하여 분석할 수 있습니다.
""")

# ✅ 탭 구성
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터 보기", "🔍 인덱스별 분석"])

# 📌 Tab 1: 데이터 요약
with tab1:
    st.header("📌 데이터 요약")
    st.dataframe(df.head())
    st.dataframe(df.describe())

# 📊 Tab 2: 전체 데이터
with tab2:
    st.header("📊 전체 데이터 보기")
    st.dataframe(df)

# 🔍 Tab 3: 정렬 + 그래프 + 다중 인덱스 선택
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    # 정렬 옵션
    sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
    ascending = st.radio("정렬 방식", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    # 히스토그램 시각화
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

    # 다중 인덱스 선택
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
