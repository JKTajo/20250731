%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Load dataset
df = kagglehub.load_dataset(
    adapter=KaggleDatasetAdapter.PANDAS,
    dataset="saurabhshahane/seoul-bike-sharing-demand-prediction",
    file="SeoulBikeData.csv",
    pandas_kwargs={"encoding": "ISO-8859-1"}
)

# 사이드바
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("Kaggle 데이터 기반")
st.sidebar.markdown(
    """
    이 앱은 서울의 자전거 대여 수요 데이터를 시각화하고,
    사용자 입력에 따라 특정 인덱스 데이터를 확인할 수 있는 기능을 제공합니다.
    """
)

# 탭 3개 생성
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터 보기", "🔍 인덱스별 분석"])

# Tab 1: 요약
with tab1:
    st.header("📌 데이터 요약")
    st.markdown("데이터셋의 기본 정보와 통계를 확인할 수 있습니다.")
    st.write("**기본 정보**")
    st.dataframe(df.head())
    st.write("**통계 요약**")
    st.dataframe(df.describe())

# Tab 2: 전체 데이터
with tab2:
    st.header("📊 전체 데이터 보기")
    st.dataframe(df)

# Tab 3: 인덱스 분석
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    sort_column = st.selectbox("정렬할 컬럼을 선택하세요", df.columns)
    ascending = st.radio("정렬 방식 선택", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    st.subheader("🎯 대여량 히스토그램")
    fig, ax = plt.subplots()
    if 'Rented Bike Count' in df.columns:
        sns.histplot(sorted_df['Rented Bike Count'], bins=30, kde=True, ax=ax)
    else:
        st.warning("⚠️ 'Rented Bike Count' 컬럼이 존재하지 않습니다.")
    st.pyplot(fig)

    index_input = st.number_input("확인할 인덱스를 입력하세요", min_value=0, max_value=len(df)-1, value=0, step=1)
    st.subheader("📌 선택된 인덱스 데이터")
    st.dataframe(sorted_df.iloc[[int(index_input)]])
