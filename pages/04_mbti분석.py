import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -----------------------------------------
# 페이지 기본 설정
# -----------------------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 세계 국가별 MBTI 비율 분석")
st.write("국가를 선택하면 해당 국가의 16가지 MBTI 비율을 막대그래프로 확인할 수 있습니다.")

MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# -----------------------------------------
# 데이터 불러오기
# Streamlit Cloud에 CSV 파일도 함께 업로드하세요.
# -----------------------------------------
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)

    required_columns = ["Country"] + MBTI_TYPES
    missing = [col for col in required_columns if col not in data.columns]

    if missing:
        raise ValueError(
            "CSV 파일에 필요한 열이 없습니다: " + ", ".join(missing)
        )

    data["Country"] = data["Country"].astype(str).str.strip()

    for col in MBTI_TYPES:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=required_columns)
    data = data[data["Country"] != ""]

    return data

st.sidebar.header("📂 데이터 파일")

default_file = Path(__file__).parent / "countriesMBTI_16types (2).csv"
uploaded_file = st.sidebar.file_uploader(
    "CSV 파일을 선택해도 됩니다.",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    elif default_file.exists():
        df = load_data(default_file)
    else:
        st.warning(
            "CSV 파일을 찾을 수 없습니다. "
            "프로젝트 폴더에 countriesMBTI_16types (2).csv 파일을 넣거나 "
            "왼쪽 메뉴에서 CSV 파일을 업로드하세요."
        )
        st.stop()
except Exception as error:
    st.error(f"데이터를 읽는 중 오류가 발생했습니다: {error}")
    st.stop()

if df.empty:
    st.error("분석할 데이터가 없습니다. CSV 파일 내용을 확인해주세요.")
    st.stop()

# -----------------------------------------
# 상단 요약
# -----------------------------------------
metric1, metric2 = st.columns(2)
metric1.metric("분석 국가 수", f"{df['Country'].nunique():,}개")
metric2.metric("MBTI 유형 수", "16개")

st.divider()

# -----------------------------------------
# 국가 선택
# -----------------------------------------
countries = sorted(df["Country"].unique().tolist())

selected_country = st.selectbox(
    "국가 선택",
    countries,
    index=0,
    help="분석하고 싶은 국가를 선택하세요."
)

country_row = df.loc[df["Country"] == selected_country].iloc[0]

# 비율은 원본 데이터가 0~1 소수이면 백분율로 변환
values = pd.to_numeric(
    country_row[MBTI_TYPES],
    errors="coerce"
).astype(float)

if values.max() <= 1:
    values = values * 100

chart_data = pd.DataFrame({
    "MBTI": MBTI_TYPES,
    "비율": values.values
}).sort_values("비율", ascending=False).reset_index(drop=True)

# 1위는 분홍색, 나머지는 진회색에서 연회색으로 점차 흐려지는 색상
gray_palette = [
    "#777777", "#858585", "#939393", "#A1A1A1",
    "#AFAFAF", "#BDBDBD", "#CBCBCB", "#D9D9D9",
    "#E2E2E2", "#E8E8E8", "#EEEEEE", "#F1F1F1",
    "#F3F3F3", "#F5F5F5", "#F7F7F7"
]
bar_colors = ["#F27BAA"] + gray_palette[:len(chart_data) - 1]

# -----------------------------------------
# 최고 비율 표시
# -----------------------------------------
top_mbti = chart_data.iloc[0]

st.subheader(f"📊 {selected_country}의 MBTI 비율")
top_col1, top_col2 = st.columns(2)
top_col1.metric("가장 높은 MBTI", top_mbti["MBTI"])
top_col2.metric("1위 비율", f"{top_mbti['비율']:.2f}%")

# -----------------------------------------
# 막대그래프
# -----------------------------------------
fig = go.Figure()

fig.add_trace(go.Bar(
    x=chart_data["비율"],
    y=chart_data["MBTI"],
    orientation="h",
    marker=dict(
        color=bar_colors,
        line=dict(width=0)
    ),
    text=[f"{v:.2f}%" for v in chart_data["비율"]],
    textposition="outside",
    cliponaxis=False,
    hovertemplate="<b>%{y}</b><br>비율: %{x:.2f}%<extra></extra>"
))

fig.update_layout(
    height=650,
    title=dict(
        text=f"{selected_country} · MBTI 분포",
        x=0.02,
        xanchor="left"
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
    margin=dict(l=35, r=65, t=75, b=45),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.caption("분홍색 막대는 선택한 국가에서 비율이 가장 높은 MBTI 유형입니다. 나머지는 회색 계열로 표시됩니다.")

# -----------------------------------------
# 순위 표
# -----------------------------------------
with st.expander("📋 MBTI 비율 순위 자세히 보기"):
    display_data = chart_data.copy()
    display_data.insert(0, "순위", range(1, len(display_data) + 1))
    display_data["비율"] = display_data["비율"].map(lambda x: f"{x:.2f}%")
    st.dataframe(display_data, use_container_width=True, hide_index=True)

st.divider()
st.caption("세계 국가별 MBTI 데이터 시각화 프로젝트")
