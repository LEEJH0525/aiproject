
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -----------------------------------------
# 1. 페이지 설정
# -----------------------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 세계 국가별 MBTI 비율 분석")
st.write(
    "국가를 선택하면 해당 국가의 16가지 MBTI 비율을 "
    "막대그래프로 확인할 수 있습니다."
)

# -----------------------------------------
# 2. 파일 경로 설정
# pages 폴더의 상위 폴더에서 CSV 찾기
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "countriesMBTI_16types (2).csv"

# -----------------------------------------
# 3. MBTI 유형
# -----------------------------------------
MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# -----------------------------------------
# 4. 데이터 불러오기
# -----------------------------------------
@st.cache_data
def load_data(file_path):

    df = pd.read_csv(file_path)

    required_columns = ["Country"] + MBTI_TYPES

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"CSV 파일에 필요한 열이 없습니다: {missing}"
        )

    df["Country"] = df["Country"].astype(str).str.strip()

    for col in MBTI_TYPES:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    df = df.dropna(
        subset=required_columns
    )

    df = df[df["Country"] != ""]

    return df


# -----------------------------------------
# 5. 데이터 오류 확인
# -----------------------------------------
if not CSV_PATH.exists():

    st.error(
        "CSV 파일을 찾을 수 없습니다.\n\n"
        f"파일 경로: {CSV_PATH}"
    )

    st.stop()

try:
    df = load_data(str(CSV_PATH))

except Exception as e:

    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


if df.empty:
    st.error("분석할 데이터가 없습니다.")
    st.stop()


# -----------------------------------------
# 6. 상단 통계
# -----------------------------------------
col1, col2 = st.columns(2)

col1.metric(
    "🌎 분석 국가 수",
    f"{df['Country'].nunique()}개"
)

col2.metric(
    "🧠 MBTI 유형 수",
    "16개"
)

st.divider()


# -----------------------------------------
# 7. 국가 선택
# -----------------------------------------
countries = sorted(
    df["Country"].unique().tolist()
)

selected_country = st.selectbox(
    "🌍 분석할 국가를 선택하세요",
    countries
)

country_row = df[
    df["Country"] == selected_country
].iloc[0]


# -----------------------------------------
# 8. MBTI 비율 계산
# -----------------------------------------
values = pd.to_numeric(
    country_row[MBTI_TYPES],
    errors="coerce"
).astype(float)

# 0~1 사이의 소수이면 백분율로 변환
if values.max() <= 1:
    values = values * 100


chart_data = pd.DataFrame({
    "MBTI": MBTI_TYPES,
    "비율": values.values
})

# 높은 비율부터 정렬
chart_data = chart_data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)


# -----------------------------------------
# 9. 그래프 색상 설정
# 1위: 분홍색
# 나머지: 진회색에서 연회색으로
# -----------------------------------------
gray_palette = [
    "#777777",
    "#858585",
    "#939393",
    "#A1A1A1",
    "#AFAFAF",
    "#BDBDBD",
    "#CBCBCB",
    "#D9D9D9",
    "#E2E2E2",
    "#E8E8E8",
    "#EEEEEE",
    "#F1F1F1",
    "#F3F3F3",
    "#F5F5F5",
    "#F7F7F7"
]

bar_colors = [
    "#F27BAA"
] + gray_palette[:len(chart_data) - 1]


# -----------------------------------------
# 10. 1위 MBTI 표시
# -----------------------------------------
top_mbti = chart_data.iloc[0]

st.subheader(
    f"📊 {selected_country}의 MBTI 분포"
)

col1, col2 = st.columns(2)

col1.metric(
    "🏆 가장 높은 MBTI",
    top_mbti["MBTI"]
)

col2.metric(
    "📈 1위 비율",
    f"{top_mbti['비율']:.2f}%"
)


# -----------------------------------------
# 11. 막대그래프
# -----------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_data["비율"],
        y=chart_data["MBTI"],
        orientation="h",

        marker=dict(
            color=bar_colors,
            line=dict(width=0)
        ),

        text=[
            f"{v:.2f}%"
            for v in chart_data["비율"]
        ],

        textposition="outside",
        cliponaxis=False,

        hovertemplate=(
            "<b>%{y}</b><br>"
            "비율: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)


# -----------------------------------------
# 12. 그래프 디자인
# -----------------------------------------
fig.update_layout(

    height=650,

    title=dict(
        text=f"{selected_country} · MBTI 비율",
        x=0.02
    ),

    xaxis=dict(
        title="비율 (%)",
        showgrid=True,
        gridcolor="#EEEEEE",
        zeroline=False
    ),

    yaxis=dict(
        title="",
        autorange="reversed",
        tickfont=dict(size=13)
    ),

    plot_bgcolor="white",
    paper_bgcolor="white",

    margin=dict(
        l=35,
        r=65,
        t=75,
        b=45
    ),

    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------------
# 13. 색상 설명
# -----------------------------------------
st.markdown(
    """
    <div style="
        padding:12px;
        background-color:#FAFAFA;
        border-radius:10px;
        font-size:14px;
    ">
    <span style="color:#F27BAA;">●</span>
    1위 MBTI &nbsp;&nbsp;
    <span style="color:#999999;">●</span>
    나머지 MBTI (회색 그라데이션)
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# 14. MBTI 순위표
# -----------------------------------------
with st.expander("📋 MBTI 비율 순위 자세히 보기"):

    display_data = chart_data.copy()

    display_data.insert(
        0,
        "순위",
        range(1, len(display_data) + 1)
    )

    display_data["비율"] = display_data[
        "비율"
    ].map(lambda x: f"{x:.2f}%")

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------------
# 15. 데이터 다운로드
# -----------------------------------------
st.divider()

st.subheader("📥 분석 결과 다운로드")

download_df = chart_data.copy()

download_df["비율"] = download_df[
    "비율"
].round(2)

csv = download_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="MBTI 분석 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_country}_MBTI_analysis.csv",
    mime="text/csv"
)


# -----------------------------------------
# 16. 하단 안내
# -----------------------------------------
st.divider()

st.caption(
    "세계 국가별 MBTI 데이터 시각화 프로젝트"
)
