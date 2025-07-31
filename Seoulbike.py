import os
import kagglehub
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Kaggle 데이터 다운로드
path = kagglehub.dataset_download("saurabhshahane/seoul-bike-sharing-demand-prediction")
st.write("📁 데이터가 저장된 경로:", path)

# Step 2: 파일 경로 찾기 (.csv)
csv_file = None
for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_file = os.path.join(path, file)
        break

if not csv_file:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.stop()

# Step 3: 데이터 불러오기
df = pd.read_csv(csv_file)

# 사이드바
st.sidebar.title("🚲 서울 자전거 수요 예측")
st.sidebar.subheader("KaggleHub 기반 Streamlit 앱")
st.sidebar.markdown("""
이 앱은 서울시 자전거 대여 수요 데이터를 기반으로 한 시각화 도구입니다.
데이터를 탐색하고 원하는 인덱스를 선택하여 분석할 수 있습니다.
""")

# 탭
tab1, tab2, tab3 = st.tabs(["📌 요약", "📊 전체 데이터 보기", "🔍 인덱스별 분석"])

# Tab 1: 요약
with tab1:
    st.header("📌 데이터 요약")
    st.subheader("데이터프레임 Preview")
    st.dataframe(df.head())
    st.subheader("통계 요약")
    st.dataframe(df.describe())

# Tab 2: 전체 테이블
with tab2:
    st.header("📊 전체 데이터 보기")
    st.dataframe(df)

# Tab 3: 정렬 + 시각화 + 다중 인덱스 선택
with tab3:
    st.header("🔍 인덱스별 분석 및 시각화")

    # 정렬 옵션
    sort_column = st.selectbox("정렬할 컬럼 선택", df.columns)
    ascending = st.radio("정렬 방식", ("오름차순", "내림차순")) == "오름차순"
    sorted_df = df.sort_values(by=sort_column, ascending=ascending)

    # 히스토그램 시각화
    st.subheader("🎯 대여량 분포 (Rented Bike Count)")
    if "Rented Bike Count" in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(sorted_df["Rented Bike Count"], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ 'Rented Bike Count' 컬럼이 없어 히스토그램을 그릴 수 없습니다.")

    # 다중 인덱스 선택
    st.subheader("📌 인덱스 선택")
    selected_indices = st.multiselect(
        "데이터 인덱스를 선택하세요",
        options=list(sorted_df.index),
        default=[0]
    )

    if selected_indices:
        st.dataframe(sorted_df.loc[selected_indices])
    else:
        st.info("인덱스를 하나 이상 선택해주세요.")
