
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울시 남녀 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 자치구별 남녀 인구 분석")
st.write("연도와 자치구를 선택하면 남자와 여자 연령별 인구를 비교합니다.")

# ==========================================
# 2. CSV 파일 경로
# ==========================================

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

    # 서울특별시 전체 행 제거
    data = data[
        data["행정구역"] != "서울특별시"
    ].copy()

    # 자치구 이름만 표시
    data["행정구역"] = (
        data["행정구역"]
        .str.replace("서울특별시 ", "", regex=False)
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

    st.error(f"데이터 오류: {e}")
    st.stop()

# ==========================================
# 4. 연도와 행정구역 선택
# ==========================================

st.subheader("🔍 분석 조건 선택")

col1, col2 = st.columns(2)

with col1:

    selected_year = st.selectbox(
        "📅 연도 선택",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

with col2:

    area_list = sorted(df["행정구역"].tolist())

    selected_area = st.selectbox(
        "📍 자치구 선택",
        area_list
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
# 6. 선택한 자치구 데이터 가져오기
# ==========================================

selected_data = df[
    df["행정구역"] == selected_area
]

if selected_data.empty:

    st.error("선택한 자치구 데이터가 없습니다.")
    st.stop()

selected_data = selected_data.iloc[0]

# ==========================================
# 7. 남자와 여자 인구 데이터 생성
# ==========================================

male_population = []
female_population = []

for age in age_list:

    male_col = (
        f"{selected_year}년_남_거주자_{age}"
    )

    female_col = (
        f"{selected_year}년_여_거주자_{age}"
    )

    if male_col not in df.columns or female_col not in df.columns:

        st.error(
            f"데이터 컬럼을 찾을 수 없습니다: {male_col}, {female_col}"
        )
        st.stop()

    male_population.append(
        selected_data[male_col]
    )

    female_population.append(
        selected_data[female_col]
    )

# 데이터프레임 생성
chart_df = pd.DataFrame({

    "연령대": age_list,
    "남자": male_population,
    "여자": female_population

})

chart_df = chart_df.fillna(0)

# ==========================================
# 8. 남녀 인구 합계
# ==========================================

male_total = chart_df["남자"].sum()
female_total = chart_df["여자"].sum()

st.divider()

st.subheader("📌 인구 분석 결과")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "선택 자치구",
        selected_area
    )

with col2:

    st.metric(
        "👨 남자 인구",
        f"{male_total:,.0f}명"
    )

with col3:

    st.metric(
        "👩 여자 인구",
        f"{female_total:,.0f}명"
    )

# ==========================================
# 9. 남녀 연령별 꺾은선 그래프
# ==========================================

st.divider()

st.subheader("📈 남녀 연령별 인구 비교")

# 세로축 최대값 계산
max_population = max(
    chart_df["남자"].max(),
    chart_df["여자"].max()
)

y_max = max(
    1000,
    math.ceil(max_population / 1000) * 1000
)

fig = go.Figure()

# 남자 그래프 - 핑크색
fig.add_trace(

    go.Scatter(

        x=chart_df["연령대"],
        y=chart_df["남자"],

        mode="lines+markers",

        name="남자",

        line=dict(
            color="#FF69B4",
            width=4
        ),

        marker=dict(
            color="#FF69B4",
            size=9
        ),

        hovertemplate=
        "연령대: %{x}<br>" +
        "남자: %{y:,.0f}명" +
        "<extra></extra>"

    )

)

# 여자 그래프 - 초록색
fig.add_trace(

    go.Scatter(

        x=chart_df["연령대"],
        y=chart_df["여자"],

        mode="lines+markers",

        name="여자",

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
        "여자: %{y:,.0f}명" +
        "<extra></extra>"

    )

)

# 그래프 디자인
fig.update_layout(

    title=dict(
        text=f"{selected_area} {selected_year}년 남녀 연령별 인구 비교",
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

    height=600,

    hovermode="x unified",

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        size=13
    ),

    legend=dict(
        title="성별",
        orientation="h",
        y=1.12,
        x=0.5,
        xanchor="center"
    ),

    margin=dict(
        l=70,
        r=30,
        t=100,
        b=60
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# 10. 연령별 남녀 인구 데이터 표
# ==========================================

st.divider()

st.subheader("📋 연령별 남녀 인구 데이터")

display_df = chart_df.copy()

display_df["남자"] = display_df["남자"].apply(
    lambda x: f"{x:,.0f}명"
)

display_df["여자"] = display_df["여자"].apply(
    lambda x: f"{x:,.0f}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 11. CSV 다운로드
# ==========================================

csv_data = chart_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(

    label="📥 남녀 인구 분석 CSV 다운로드",

    data=csv_data,

    file_name=f"{selected_area}_{selected_year}_남녀인구.csv",

    mime="text/csv"

)

# ==========================================
# 12. 마무리
# ==========================================

st.divider()

st.caption(
    "서울시 자치구별 남녀 인구 분석 | Pandas + Streamlit + Plotly"
)
