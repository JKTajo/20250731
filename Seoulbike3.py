{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN/vTuS18+mZ9Y4biRVkZpl",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JKTajo/20250731/blob/main/Seoulbike3.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "id": "wC3bH50cJNma",
        "outputId": "a7190539-cd0c-4637-cc69-1ca85e3fd3a8",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/tmp/ipython-input-4270648171.py:10: DeprecationWarning: load_dataset is deprecated and will be removed in a future version.\n",
            "  df = kagglehub.load_dataset(\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "First 5 records:          Date  Rented Bike Count  Hour  Temperature(°C)  Humidity(%)  \\\n",
            "0  01/12/2017                254     0             -5.2           37   \n",
            "1  01/12/2017                204     1             -5.5           38   \n",
            "2  01/12/2017                173     2             -6.0           39   \n",
            "3  01/12/2017                107     3             -6.2           40   \n",
            "4  01/12/2017                 78     4             -6.0           36   \n",
            "\n",
            "   Wind speed (m/s)  Visibility (10m)  Dew point temperature(°C)  \\\n",
            "0               2.2              2000                      -17.6   \n",
            "1               0.8              2000                      -17.6   \n",
            "2               1.0              2000                      -17.7   \n",
            "3               0.9              2000                      -17.6   \n",
            "4               2.3              2000                      -18.6   \n",
            "\n",
            "   Solar Radiation (MJ/m2)  Rainfall(mm)  Snowfall (cm) Seasons     Holiday  \\\n",
            "0                      0.0           0.0            0.0  Winter  No Holiday   \n",
            "1                      0.0           0.0            0.0  Winter  No Holiday   \n",
            "2                      0.0           0.0            0.0  Winter  No Holiday   \n",
            "3                      0.0           0.0            0.0  Winter  No Holiday   \n",
            "4                      0.0           0.0            0.0  Winter  No Holiday   \n",
            "\n",
            "  Functioning Day  \n",
            "0             Yes  \n",
            "1             Yes  \n",
            "2             Yes  \n",
            "3             Yes  \n",
            "4             Yes  \n"
          ]
        }
      ],
      "source": [
        "# Install dependencies as needed:\n",
        "# pip install kagglehub[pandas-datasets]\n",
        "import kagglehub\n",
        "from kagglehub import KaggleDatasetAdapter\n",
        "\n",
        "# Set the path to the file you'd like to load\n",
        "file_path = \"SeoulBikeData.csv\"\n",
        "\n",
        "# Load the latest version\n",
        "df = kagglehub.load_dataset(\n",
        "  KaggleDatasetAdapter.PANDAS,\n",
        "  \"saurabhshahane/seoul-bike-sharing-demand-prediction\",\n",
        "  file_path,\n",
        "  pandas_kwargs={'encoding': 'ISO-8859-1'}\n",
        "  # Provide any additional arguments like\n",
        "  # sql_query or pandas_kwargs. See the\n",
        "  # documenation for more information:\n",
        "  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas\n",
        ")\n",
        "\n",
        "print(\"First 5 records:\", df.head())"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4c1ced7c",
        "outputId": "92c90c7e-da7b-495c-8876-95bcdd427f26"
      },
      "source": [
        "%%writefile app.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import kagglehub\n",
        "from kagglehub import KaggleDatasetAdapter\n",
        "\n",
        "# Load dataset\n",
        "file_path = \"SeoulBikeData.csv\"  # 파일 이름은 실제 데이터셋에 따라 수정 필요\n",
        "df = kagglehub.load_dataset(\n",
        "    KaggleDatasetAdapter.PANDAS,\n",
        "    \"saurabhshahane/seoul-bike-sharing-demand-prediction\",\n",
        "    file_path,\n",
        "    pandas_kwargs={'encoding': 'ISO-8859-1'}\n",
        ")\n",
        "\n",
        "# 사이드바\n",
        "st.sidebar.title(\"🚲 서울 자전거 수요 예측\")\n",
        "st.sidebar.subheader(\"Kaggle 데이터 기반\")\n",
        "st.sidebar.markdown(\n",
        "    \"\"\"\n",
        "    이 앱은 서울의 자전거 대여 수요 데이터를 시각화하고,\n",
        "    사용자 입력에 따라 특정 인덱스 데이터를 확인할 수 있는 기능을 제공합니다.\n",
        "    \"\"\"\n",
        ")\n",
        "\n",
        "# 탭 3개 생성\n",
        "tab1, tab2, tab3 = st.tabs([\"📌 요약\", \"📊 전체 데이터 보기\", \"🔍 인덱스별 분석\"])\n",
        "\n",
        "# =====================\n",
        "# 📌 Tab 1: 요약 탭\n",
        "# =====================\n",
        "with tab1:\n",
        "    st.header(\"📌 데이터 요약\")\n",
        "    st.markdown(\"데이터셋의 기본 정보와 통계를 확인할 수 있습니다.\")\n",
        "    st.write(\"**기본 정보**\")\n",
        "    st.dataframe(df.head())\n",
        "    st.write(\"**통계 요약**\")\n",
        "    st.dataframe(df.describe())\n",
        "\n",
        "# =====================\n",
        "# 📊 Tab 2: 전체 데이터\n",
        "# =====================\n",
        "with tab2:\n",
        "    st.header(\"📊 전체 데이터 보기\")\n",
        "    st.dataframe(df)\n",
        "\n",
        "# =====================\n",
        "# 🔍 Tab 3: 인덱스 지정 분석\n",
        "# =====================\n",
        "with tab3:\n",
        "    st.header(\"🔍 인덱스별 분석 및 시각화\")\n",
        "\n",
        "    # 정렬 옵션\n",
        "    sort_column = st.selectbox(\"정렬할 컬럼을 선택하세요\", df.columns)\n",
        "    ascending = st.radio(\"정렬 방식 선택\", (\"오름차순\", \"내림차순\")) == \"오름차순\"\n",
        "    sorted_df = df.sort_values(by=sort_column, ascending=ascending)\n",
        "\n",
        "    # 그래프 (예: 대여량 히스토그램)\n",
        "    st.subheader(\"🎯 대여량 히스토그램\")\n",
        "    fig, ax = plt.subplots()\n",
        "    sns.histplot(sorted_df['Rented Bike Count'], bins=30, kde=True, ax=ax)\n",
        "    st.pyplot(fig)\n",
        "\n",
        "    # 인덱스 선택\n",
        "    index_input = st.number_input(\"확인할 인덱스를 입력하세요\", min_value=0, max_value=len(df)-1, value=0, step=1)\n",
        "\n",
        "    # 선택된 인덱스 출력\n",
        "    st.subheader(\"📌 선택된 인덱스 데이터\")\n",
        "    st.dataframe(sorted_df.iloc[[index_input]])"
      ],
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "1e051889",
        "outputId": "d3a67f60-bafa-4285-d132-ca4add2656db"
      },
      "source": [
        "!streamlit run app.py"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/bin/bash: line 1: streamlit: command not found\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9ee239ee"
      },
      "source": [
        "!pip install streamlit -q\n",
        "!pip install pyngrok"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "edf24a91"
      },
      "source": [
        "from pyngrok import ngrok\n",
        "\n",
        "# Terminate open tunnels if any\n",
        "ngrok.kill()\n",
        "\n",
        "# Setting the authtoken (optional)\n",
        "# Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken\n",
        "NGROK_AUTH_TOKEN = \"\"  #@param {type:\"string\"}\n",
        "ngrok.set_auth_token(NGROK_AUTH_TOKEN)\n",
        "\n",
        "# Open a http tunnel on the default port 8501\n",
        "public_url = ngrok.connect(8501)\n",
        "print(f\"Streamlit app is running at: {public_url}\")"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "48484aa3"
      },
      "source": [
        "!streamlit run app.py &>/dev/null&"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}