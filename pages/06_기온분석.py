
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="월별 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온 분석")

st.write(
    "월을 선택하면 해당 월의 연도별 최고 기온과 "
    "최저 기온을 꺾은선그래프로 확인할 수 있습니다."
)

# ==========================================
# 2. CSV 파일 경로 설정
# ==========================================
# 현재 파이썬 파일은 pages 폴더 안에 있음
# parent.parent를 사용하면 프로젝트 최상위 폴더가 됨

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "temperature (1).csv"

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================
if not CSV_PATH.exists():
    st.error("temperature (1).csv 파일을 찾을 수 없습니다.")

    st.write("현재 파이썬 파일 위치:")
    st.code(str(Path(__file__).resolve()))

    st.write("CSV 파일을 찾는 위치:")
    st.code(str(CSV_PATH))

    st.write("프로젝트 상위 폴더의 파일 목록:")

    if BASE_DIR.exists():
        st.write([file.name for file in BASE_DIR.iterdir()])

    st.stop()

try:
    try:
        df = pd.read_csv(
            CSV_PATH,
            encoding="cp949"
        )

    except UnicodeDecodeError:
        df = pd.read_csv(
            CSV_PATH,
            encoding="utf-8-sig"
        )

except Exception as e:
    st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
    st.stop()

st.success("기온 데이터 불러오기 성공!")

# ==========================================
# 4. 필요한 열 확인
# ==========================================
required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"CSV 파일에 필요한 열이 없습니다: {missing_columns}")
    st.stop()

# ==========================================
# 5. 월 이름 설정
# ==========================================
month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

month_names = {
    1: "1월",
    2: "2월",
    3: "3월",
    4: "4월",
    5: "5월",
    6: "6월",
    7: "7월",
    8: "8월",
    9: "9월",
    10: "10월",
    11: "11월",
    12: "12월"
}

# ==========================================
# 6. 날짜 데이터 정리
# ==========================================
# 날짜 형식 예: Oct-07

date_parts = df["일시"].astype(str).str.extract(
    r"^([A-Za-z]{3})-(\d{2})$"
)

df["월번호"] = date_parts[0].map(month_map)

df["두자리연도"] = pd.to_numeric(
    date_parts[1],
    errors="coerce"
)

# ==========================================
# 7. 연도 변환
# ==========================================
# 첫 기록이 1907년이고 데이터가 시간순으로
# 정렬되어 있다는 전제에서 연도를 복원

years = []

century = 1900
previous_year = None

for yy in df["두자리연도"]:

    if pd.isna(yy):
        years.append(None)
        continue

    yy = int(yy)

    if previous_year is not None:

        if previous_year - yy > 50:
            century += 100

    years.append(century + yy)

    previous_year = yy

df["연도"] = years

# ==========================================
# 8. 기온 데이터 숫자 변환
# ==========================================
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"],
    errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"],
    errors="coerce"
)

# ==========================================
# 9. 월 선택 메뉴
# ==========================================
st.subheader("📅 분석할 월 선택")

selected_month = st.selectbox(
    "원하는 월을 선택하세요.",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x]
)

# ==========================================
# 10. 선택한 월 데이터 추출
# ==========================================
month_df = df[
    df["월번호"] == selected_month
].copy()

month_df = month_df.dropna(
    subset=[
        "연도",
        "최고기온(℃)",
        "최저기온(℃)"
    ]
)

month_df = month_df.sort_values("연도")

# ==========================================
# 11. 월별 기온 분석 그래프
# ==========================================
st.subheader("📈 월별 기온분석")

if month_df.empty:

    st.warning("선택한 월에 표시할 데이터가 없습니다.")

else:

    fig = go.Figure()

    # 최고 기온: 핫핑크
    fig.add_trace(
        go.Scatter(
            x=month_df["연도"],
            y=month_df["최고기온(℃)"],
            mode="lines+markers",
            name="최고 기온",
            line=dict(
                color="#FF1493",
                width=3
            ),
            marker=dict(
                size=7
            )
        )
    )

    # 최저 기온: 하늘색
    fig.add_trace(
        go.Scatter(
            x=month_df["연도"],
            y=month_df["최저기온(℃)"],
            mode="lines+markers",
            name="최저 기온",
            line=dict(
                color="#87CEEB",
                width=3
            ),
            marker=dict(
                size=7
            )
        )
    )

    # 그래프 제목과 축 설정
    fig.update_layout(
        title={
            "text": "월별 기온분석",
            "x": 0.5,
            "xanchor": "center"
        },

        xaxis_title="연도",

        yaxis_title="온도 (℃)",

        hovermode="x unified",

        height=600,

        template="plotly_white",

        font=dict(
            family="Arial, sans-serif",
            size=13
        ),

        legend=dict(
            title="기온 종류",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        xaxis=dict(
            tickformat="d",
            dtick=5
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # 12. 기온 통계
    # ======================================
    st.subheader(
        f"📊 {month_names[selected_month]} 기온 통계"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "평균 최고 기온",
            f"{month_df['최고기온(℃)'].mean():.1f} ℃"
        )

    with col2:
        st.metric(
            "평균 최저 기온",
            f"{month_df['최저기온(℃)'].mean():.1f} ℃"
        )

    # ======================================
    # 13. 데이터 확인
    # ======================================
    with st.expander("선택한 월의 데이터 확인하기"):

        show_df = month_df[
            [
                "연도",
                "일시",
                "최고기온(℃)",
                "최저기온(℃)"
            ]
        ].copy()

        show_df["연도"] = show_df["연도"].astype(int)

        st.dataframe(
            show_df,
            use_container_width=True,
            hide_index=True
        )

st.caption("데이터 출처: temperature (1).csv")
