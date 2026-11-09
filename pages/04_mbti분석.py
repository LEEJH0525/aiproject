
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="세계 국가별 MBTI 분석", page_icon="🌍", layout="wide")
st.title("🌍 세계 국가별 MBTI 분석")
st.write("국가별 MBTI 분포와 MBTI 유형별 국가 순위를 확인할 수 있습니다.")

# CSV는 pages 폴더의 상위 폴더에 위치
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "countriesMBTI_16types (2).csv"

MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# 데이터 불러오기
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    required = ["Country"] + MBTI_TYPES
    missing = [c for c in required if c not in data.columns]

    if missing:
        raise ValueError("CSV에 필요한 열이 없습니다: " + ", ".join(missing))

    data["Country"] = data["Country"].astype(str).str.strip()

    for mbti in MBTI_TYPES:
        data[mbti] = pd.to_numeric(data[mbti], errors="coerce")

    data = data.dropna(subset=required)
    data = data[data["Country"] != ""]
    data = data.drop_duplicates(subset=["Country"])

    return data


if not CSV_PATH.exists():
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

try:
    df = load_data(str(CSV_PATH))
except Exception as error:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {error}")
    st.stop()

if df.empty:
    st.error("분석할 데이터가 없습니다.")
    st.stop()

# 소수 비율을 퍼센트로 변환
if df[MBTI_TYPES].max().max() <= 1:
    df[MBTI_TYPES] = df[MBTI_TYPES] * 100

# 상단 통계
c1, c2, c3 = st.columns(3)
c1.metric("분석 국가 수", f"{df['Country'].nunique()}개")
c2.metric("MBTI 유형 수", "16개")
c3.metric("분석 데이터 수", f"{len(df) * 16:,}개")

st.divider()

# 분석 메뉴
menu = st.radio(
    "분석 메뉴",
    ["국가별 MBTI 분포", "MBTI별 국가 순위"],
    horizontal=True
)

# =========================================
# 1. 국가별 MBTI 분포
# =========================================
if menu == "국가별 MBTI 분포":

    st.header("🌍 국가별 MBTI 비율")

    countries = sorted(df["Country"].unique().tolist())

    country = st.selectbox("국가 선택", countries)

    row = df[df["Country"] == country].iloc[0]

    result = pd.DataFrame({
        "MBTI": MBTI_TYPES,
        "비율": [float(row[m]) for m in MBTI_TYPES]
    }).sort_values("비율", ascending=False).reset_index(drop=True)

    best = result.iloc[0]

    a, b = st.columns(2)
    a.metric("가장 높은 MBTI", best["MBTI"])
    b.metric("1위 비율", f"{best['비율']:.2f}%")

    # 1위 분홍색, 나머지 회색 그라데이션
    gray_colors = [
        "#858585", "#929292", "#9F9F9F",
        "#ACACAC", "#B9B9B9", "#C6C6C6",
        "#D0D0D0", "#D8D8D8", "#DFDFDF",
        "#E5E5E5", "#EAEAEA", "#EEEEEE",
        "#F1F1F1", "#F4F4F4", "#F7F7F7"
    ]

    colors = ["#F27BAA"] + gray_colors[:len(result) - 1]

    fig = go.Figure(go.Bar(
        x=result["비율"],
        y=result["MBTI"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.2f}%" for v in result["비율"]],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>비율: %{x:.2f}%<extra></extra>"
    ))

    fig.update_layout(
        height=650,
        title=f"{country}의 MBTI 비율",
        xaxis_title="비율 (%)",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=35, r=65, t=70, b=45)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("1위는 분홍색, 나머지는 진회색에서 연회색으로 표시됩니다.")

    with st.expander("📋 국가별 MBTI 순위표"):
        table = result.copy()
        table.insert(0, "순위", range(1, len(table) + 1))
        table["비율"] = table["비율"].map(lambda x: f"{x:.2f}%")
        st.dataframe(table, use_container_width=True, hide_index=True)


# =========================================
# 2. MBTI별 국가 순위
# =========================================
elif menu == "MBTI별 국가 순위":

    st.header("🧠 MBTI 유형별 국가 순위")

    st.write(
        "MBTI 하나를 선택하면 비율이 높은 국가부터 "
        "낮은 국가까지 자동으로 정렬됩니다."
    )

    selected_mbti = st.selectbox(
        "MBTI 유형 선택",
        MBTI_TYPES
    )

    ranking = df[["Country", selected_mbti]].copy()

    ranking = ranking.rename(
        columns={selected_mbti: "비율"}
    )

    ranking = ranking.sort_values(
        "비율",
        ascending=False
    ).reset_index(drop=True)

    ranking.insert(
        0,
        "순위",
        range(1, len(ranking) + 1)
    )

    # 최고 국가와 최저 국가
    highest = ranking.iloc[0]
    lowest = ranking.iloc[-1]

    a, b, c = st.columns(3)

    a.metric(
        "🥇 가장 높은 국가",
        highest["Country"],
        f"{highest['비율']:.2f}%"
    )

    b.metric(
        "🔵 가장 낮은 국가",
        lowest["Country"],
        f"{lowest['비율']:.2f}%"
    )

    c.metric(
        "🌎 비교 국가 수",
        f"{len(ranking)}개"
    )

    # 분홍색에서 파란색으로 색상 그라데이션
    def gradient_color(start_hex, end_hex, ratio):

        start = tuple(
            int(start_hex[i:i+2], 16)
            for i in (1, 3, 5)
        )

        end = tuple(
            int(end_hex[i:i+2], 16)
            for i in (1, 3, 5)
        )

        rgb = tuple(
            round(
                start[j] +
                (end[j] - start[j]) * ratio
            )
            for j in range(3)
        )

        return "#{:02X}{:02X}{:02X}".format(*rgb)

    pink = "#F27BAA"
    blue = "#6599E8"

    if len(ranking) == 1:
        bar_colors = [pink]
    else:
        bar_colors = [
            gradient_color(
                pink,
                blue,
                i / (len(ranking) - 1)
            )
            for i in range(len(ranking))
        ]

    # 국가별 막대그래프
    fig = go.Figure(go.Bar(
        x=ranking["비율"],
        y=ranking["Country"],
        orientation="h",

        marker=dict(
            color=bar_colors,
            line=dict(width=0)
        ),

        text=[
            f"{v:.2f}%"
            for v in ranking["비율"]
        ],

        textposition="outside",
        cliponaxis=False,

        hovertemplate=(
            "<b>%{y}</b><br>" +
            selected_mbti +
            " 비율: %{x:.2f}%<extra></extra>"
        )
    ))

    fig.update_layout(
        height=max(650, len(ranking) * 24),
        title=f"{selected_mbti} 비율 국가별 순위",
        xaxis_title="비율 (%)",
        yaxis_title="국가",

        # 가장 높은 국가를 맨 위에 표시
        yaxis=dict(autorange="reversed"),

        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,

        margin=dict(
            l=130,
            r=75,
            t=70,
            b=45
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "분홍색일수록 비율이 높고, 파란색일수록 비율이 낮습니다."
    )

    # 전체 순위표
    st.subheader(f"📋 {selected_mbti} 전체 국가 순위표")

    display_ranking = ranking.copy()

    display_ranking["비율"] = display_ranking[
        "비율"
    ].map(lambda x: f"{x:.2f}%")

    st.dataframe(
        display_ranking,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    # CSV 다운로드
    csv_data = ranking.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label=f"📥 {selected_mbti} 국가 순위 CSV 다운로드",
        data=csv_data,
        file_name=f"{selected_mbti}_country_ranking.csv",
        mime="text/csv"
    )


# 하단 안내
st.divider()

st.caption(
    "세계 국가별 MBTI 데이터 분석 | Streamlit Cloud"
)
