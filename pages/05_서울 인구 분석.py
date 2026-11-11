
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울시 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령별 인구 분석")
st.write("행정구역, 연도, 성별을 선택하여 연령별 인구를 분석합니다.")

# ==========================================
# 2. CSV 파일 경로 설정
# ==========================================

# 현재 py 파일은 pages 폴더에 있고
# CSV 파일은 그 상위 폴더에 있음

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "population.csv"

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    try:
        data = pd.read_csv(
            CSV_PATH,
            encoding="cp949"
        )

    except UnicodeDecodeError:
        data = pd.read_csv(
            CSV_PATH,
            encoding="utf-8-sig"
        )

    # 행정구역 이름 정리
    data["행정구역"] = (
        data["행정구역"]
        .astype(str)
        .str.replace(r"\s*\(\d+\)", "", regex=True)
        .str.strip()
    )

    # 숫자 데이터 변환
    for col in data.columns:

        if col != "행정구역":

            data[col] = pd.to_numeric(
                data[col]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

except Exception as e:

    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ==========================================
# 4. 분석 조건 선택
# ==========================================

st.subheader("🔍 분석 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:

    area_list = df["행정구역"].tolist()

    selected_area = st.selectbox(
        "행정구역 선택",
        area_list
    )

with col2:

    selected_year = st.selectbox(
        "연도 선택",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

with col3:

    selected_gender = st.selectbox(
        "성별 선택",
        ["전체", "남자", "여자"]
    )

# ==========================================
# 5. 연령대 설정
# ==========================================

age_list = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

# ==========================================
# 6. 성별 컬럼 설정
# ==========================================

if selected_gender == "전체":

    gender_prefix = ""

elif selected_gender == "남자":

    gender_prefix = "남_"

else:

    gender_prefix = "여_"

# ==========================================
# 7. 선택한 행정구역 데이터 가져오기
# ==========================================

selected_data = df[
    df["행정구역"] == selected_area
]

if selected_data.empty:

    st.error("선택한 행정구역 데이터가 없습니다.")
    st.stop()

selected_data = selected_data.iloc[0]

# ==========================================
# 8. 연령별 인구 데이터 생성
# ==========================================

population_list = []

for age in age_list:

    column_name = (
        f"{selected_year}년_"
        f"{gender_prefix}거주자_{age}"
    )

    if column_name not in df.columns:

        st.error(
            f"데이터 컬럼을 찾을 수 없습니다: {column_name}"
        )
        st.stop()

    population_list.append(
        selected_data[column_name]
    )

chart_df = pd.DataFrame({

    "연령대": age_list,
    "인구수": population_list

})

chart_df["인구수"] = chart_df["인구수"].fillna(0)

# ==========================================
# 9. 인구 통계
# ==========================================

total_population = chart_df["인구수"].sum()

st.divider()

st.subheader("📌 분석 결과")

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "행정구역",
        selected_area
    )

with m2:

    st.metric(
        "선택 연도",
        f"{selected_year}년"
    )

with m3:

    st.metric(
        "연령별 인구 합계",
        f"{total_population:,.0f}명"
    )

# ==========================================
# 10. 초록색 꺾은선 그래프
# ==========================================

st.divider()

st.subheader("📈 연령별 인구 꺾은선 그래프")

max_population = chart_df["인구수"].max()

y_max = max(
    1000,
    math.ceil(max_population / 1000) * 1000
)

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=chart_df["연령대"],
        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color="green",
            width=4
        ),

        marker=dict(
            color="green",
            size=9
        ),

        hovertemplate=
        "연령대: %{x}<br>" +
        "인구수: %{y:,.0f}명" +
        "<extra></extra>"

    )

)

fig.update_layout(

    title=dict(
        text=f"{selected_area} {selected_year}년 {selected_gender} 연령별 인구",
        x=0.5
    ),

    xaxis=dict(
        title="나이",
        tickangle=0
    ),

    yaxis=dict(
        title="인구수 (명)",
        range=[0, y_max],
        dtick=1000,
        tickformat=",",
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1
    ),

    height=550,

    hovermode="x unified",

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        size=13
    ),

    margin=dict(
        l=70,
        r=30,
        t=80,
        b=60
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# 11. 연령별 인구 데이터 표
# ==========================================

st.divider()

st.subheader("📋 연령별 인구 데이터")

display_df = chart_df.copy()

display_df["인구수"] = display_df["인구수"].apply(
    lambda x: f"{x:,.0f}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 12. CSV 다운로드
# ==========================================

csv_data = chart_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(

    label="📥 분석 결과 CSV 다운로드",

    data=csv_data,

    file_name="서울시_연령별_인구분석.csv",

    mime="text/csv"

)

# ==========================================
# 13. 마무리
# ==========================================

st.divider()

st.caption(
    "서울시 인구 데이터 분석 | Pandas + Streamlit + Plotly"
)
