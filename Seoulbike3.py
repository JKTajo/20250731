# %%writefile app.py  ← Colab에서만 필요. 로컬에서는 제거해도 됨
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kagglehub import load_dataset, KaggleDatasetAdapter

# =====================
# 데이터 불러오기
# =====================
@st.cache_data
def load_data():
    df = load_dataset(
        adapter=KaggleDatasetAdapter.PANDAS,
        dataset="saurabhshahane/seoul-bike-sharing-demand-prediction",
        file="SeoulBikeData.csv",
        pandas_kwargs={"encoding": "ISO-8859-1"}
    )
    return df

df = load_data()

# =====================
# 사이드바 설정
# =====================
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("Kaggle 데이터 기반")
st.sidebar.markdown(
    """
    이 앱은 서울의 자전거 대여 수요 데이터를 시각화하고,  
    사용자 입력에 따라 특정 인덱스 데이터를 확인할 수 있는 기능을 제공합니다.
    """
)

# =====================
# 탭 구성
# =====================
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터 보기", "🔍 인덱스별 분석"])

# =====================
# Tab 1: 요약
# =====================
with tab1:
    st.header("📌 데이터 요약")
    st.write("**기본 정보**")
    st.dataframe(df.head())
    st.write("**통계 요약**")
    st.dataframe(df.describe())

# =====================
# Tab 2: 전체 데이터 보기
# =====================
with tab2:
    st.header("📊 전체 데이터 보기")
    st.dataframe(df)

# =====================
# Tab 3: 인덱스별 분석
# =====================
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    sort_column = st.selectbox("정렬할 컬럼을 선택하세요", df.columns)
    ascending = st.radio("정렬 방식 선택", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    st.subheader("🎯 대여량 히스토그램")

    # 안전하게 컬럼명 확인
    target_column = 'Rented Bike Count'
    if target_column in sorted_df.columns:
        fig, ax = plt.subplots()
        sns.histplot(sorted_df[target_column], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"'{target_column}' 컬럼이 존재하지 않습니다. 현재 컬럼들: {df.columns.tolist()}")

    st.subheader("📌 선택한 인덱스 정보")
    index_input = st.number_input("확인할 인덱스를 입력하세요", min_value=0, max_value=len(df)-1, value=0, step=1)
    st.dataframe(sorted_df.iloc[[int(index_input)]])
