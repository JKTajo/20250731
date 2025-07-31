{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOnRwbsUwnNvFXPJpXU3oT6",
      "include_colab_link": True
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
        "<a href=\"https://colab.research.google.com/github/JKTajo/20250731/blob/main/seoulbike2.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {
        "id": "S6YUEsBO7ItX"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "import pandas as pd\n",
        "import streamlit as st\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import kagglehub\n",
        "\n",
        "# ✅ 한글 폰트 설정 (Mac 내장 폰트)\n",
        "plt.rcParams['font.family'] = 'AppleGothic'\n",
        "\n",
        "# ✅ KaggleHub에서 데이터 다운로드\n",
        "path = kagglehub.dataset_download(\"saurabhshahane/seoul-bike-sharing-demand-prediction\")\n",
        "\n",
        "# ✅ CSV 파일 찾기\n",
        "csv_file = None\n",
        "for file in os.listdir(path):\n",
        "    if file.endswith(\".csv\"):\n",
        "        csv_file = os.path.join(path, file)\n",
        "        break\n",
        "\n",
        "if not csv_file:\n",
        "    st.error(\"❌ CSV 파일을 찾을 수 없습니다.\")\n",
        "    st.stop()\n",
        "\n",
        "# ✅ 데이터 불러오기\n",
        "df = pd.read_csv(csv_file)\n",
        "\n",
        "# ✅ 사이드바\n",
        "st.sidebar.title(\"🚲 서울 자전거 수요 예측\")\n",
        "st.sidebar.subheader(\"KaggleHub 기반 Streamlit 앱\")\n",
        "st.sidebar.markdown(\"\"\"\n",
        "이 앱은 서울시 자전거 대여 수요 데이터를 기반으로 한 시각화 도구입니다.\n",
        "데이터를 탐색하고 원하는 인덱스를 선택하여 분석할 수 있습니다.\n",
        "\"\"\")\n",
        "\n",
        "# ✅ 탭 구성\n",
        "tab1, tab2, tab3 = st.tabs([\"📌 요약\", \"📊 전체 데이터 보기\", \"🔍 인덱스별 분석\"])\n",
        "\n",
        "# 📌 Tab 1: 데이터 요약\n",
        "with tab1:\n",
        "    st.header(\"📌 데이터 요약\")\n",
        "    st.dataframe(df.head())\n",
        "    st.dataframe(df.describe())\n",
        "\n",
        "# 📊 Tab 2: 전체 데이터\n",
        "with tab2:\n",
        "    st.header(\"📊 전체 데이터 보기\")\n",
        "    st.dataframe(df)\n",
        "\n",
        "# 🔍 Tab 3: 정렬 + 그래프 + 다중 인덱스 선택\n",
        "with tab3:\n",
        "    st.header(\"🔍 인덱스별 분석 및 시각화\")\n",
        "\n",
        "    # 정렬 옵션\n",
        "    sort_column = st.selectbox(\"정렬할 컬럼 선택\", df.columns)\n",
        "    ascending = st.radio(\"정렬 방식\", (\"오름차순\", \"내림차순\")) == \"오름차순\"\n",
        "    sorted_df = df.sort_values(by=sort_column, ascending=ascending)\n",
        "\n",
        "    # 히스토그램 시각화 (한글 폰트 적용됨)\n",
        "    if \"Rented Bike Count\" in df.columns:\n",
        "        st.subheader(\"🎯 대여량 분포\")\n",
        "        fig, ax = plt.subplots()\n",
        "        sns.histplot(sorted_df[\"Rented Bike Count\"], bins=30, kde=True, ax=ax)\n",
        "        ax.set_title(\"자전거 대여량 히스토그램\")\n",
        "        ax.set_xlabel(\"대여 수\")\n",
        "        ax.set_ylabel(\"빈도\")\n",
        "        st.pyplot(fig)\n",
        "    else:\n",
        "        st.warning(\"⚠️ 'Rented Bike Count' 컬럼이 없어 히스토그램을 그릴 수 없습니다.\")\n",
        "\n",
        "    # 다중 인덱스 선택\n",
        "    st.subheader(\"📌 원하는 인덱스 선택\")\n",
        "    selected_indices = st.multiselect(\n",
        "        \"데이터 인덱스를 선택하세요\",\n",
        "        options=list(sorted_df.index),\n",
        "        default=[0]\n",
        "    )\n",
        "\n",
        "    if selected_indices:\n",
        "        st.dataframe(sorted_df.loc[selected_indices])\n",
        "    else:\n",
        "        st.info(\"인덱스를 하나 이상 선택해주세요.\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 378
        },
        "id": "nNhOYty37Nh8",
        "outputId": "eedcc4a7-c7c8-4b0f-9556-92d5e37adf2d"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-82177736.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mos\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mmatplotlib\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpyplot\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mplt\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mseaborn\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0msns\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ]
    }
  ]
}
