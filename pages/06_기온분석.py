
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
st.write("월을 선택하면 해당 월의 연도별 최고 기온과 최저 기온을 비교할 수 있습니다.")

# ==========================================
# 2. CSV 파일 불러오기
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "temperature.csv"

try:
    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("app.py와 같은 폴더에 temperature.csv 파일을 넣어주세요.")
    st.stop()

# ==========================================
# 3. 필요한 데이터 확인
# ==========================================
required_columns = ["일시", "최고기온(℃)", "최저기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일에 필요한 열이 없습니다.")
    st.write("필요한 열:", required_columns)
    st.stop()

# ==========================================
# 4. 날짜 데이터 정리
# ==========================================
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

# 날짜 형식: Oct-07
date_parts = df["일시"].astype(str).str.extract(
    r"^([A-Za-z]{3})-(\d{2})$"
)

df["월번호"] = date_parts[0].map(month_map)
df["두자리연도"] = pd.to_numeric(date_parts[1], errors="coerce")

# 데이터가 시간순으로 정렬되어 있다는 전제에서
# 99년에서 00년으로 넘어갈 때 세기를 변경
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

# 기온 데이터 숫자 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"], errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"], errors="coerce"
)

# ==========================================
# 5. 월 선택 메뉴
# ==========================================
st.subheader("📅 분석할 월 선택")

selected_month = st.selectbox(
    "원하는 월을 선택하세요.",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x]
)

# 선택한 월 데이터만 추출
month_df = df[df["월번호"] == selected_month].copy()

# 그래프에 필요한 데이터가 있는 행만 사용
month_df = month_df.dropna(
    subset=["연도", "최고기온(℃)", "최저기온(℃)"]
)

# 연도 순서대로 정렬
month_df = month_df.sort_values("연도")

# ==========================================
# 6. 월별 기온 분석 그래프
# ==========================================
st.subheader("📈 월별 기온분석")

if month_df.empty:
    st.warning("선택한 월에 표시할 데이터가 없습니다.")

else:
    fig = go.Figure()

    # 최고 기온 - 핫핑크
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
            marker=dict(size=6)
        )
    )

    # 최저 기온 - 하늘색
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
            marker=dict(size=6)
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
    # 7. 기온 통계
    # ======================================
    st.subheader(f"📊 {month_names[selected_month]} 기온 통계")

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
    # 8. 데이터 표
    # ======================================
    with st.expander("선택한 월의 데이터 확인하기"):
        show_df = month_df[
            ["연도", "일시", "최고기온(℃)", "최저기온(℃)"]
        ].copy()

        show_df["연도"] = show_df["연도"].astype(int)

        st.dataframe(
            show_df,
            use_container_width=True,
            hide_index=True
        )

st.caption("데이터 출처: 업로드한 temperature.csv 파일")
