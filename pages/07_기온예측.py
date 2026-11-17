
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="기온 분석 및 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월평균 기온 분석 및 미래 예측")
st.write(
    "과거 기온 데이터를 바탕으로 선형회귀 알고리즘을 학습하고 "
    "미래의 평균 기온을 예측합니다."
)

st.divider()


# ==========================================
# 2. CSV 파일 자동 찾기
# ==========================================
def find_csv_file():

    current_folder = Path(__file__).resolve().parent

    # app.py가 pages 폴더에 있을 경우와
    # 최상위 폴더에 있을 경우 모두 대응
    folders = [
        current_folder,
        current_folder.parent
    ]

    possible_names = [
        "temperature.csv",
        "temperature (2).csv",
        "tempre.csv",
        "tempre (2).csv"
    ]

    # 지정된 파일명 먼저 검색
    for folder in folders:
        for filename in possible_names:
            file_path = folder / filename

            if file_path.exists():
                return file_path

    # temperature로 시작하는 CSV 파일 자동 검색
    for folder in folders:
        if folder.exists():
            for file_path in folder.glob("*.csv"):
                if file_path.stem.lower().startswith(
                    ("temperature", "tempre")
                ):
                    return file_path

    return None


# ==========================================
# 3. 데이터 불러오기
# ==========================================
@st.cache_data
def load_data(file_path):

    encodings = [
        "cp949",
        "utf-8-sig",
        "euc-kr",
        "utf-8"
    ]

    data = None

    for encoding in encodings:
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding
            )
            break

        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError("CSV 파일의 인코딩을 확인해주세요.")

    # 필수 컬럼 확인
    required_columns = [
        "일시",
        "평균기온(℃)"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"CSV 파일에 '{column}' 컬럼이 없습니다."
            )

    # 날짜 변환
    # Oct-07 형식을 2007년 10월로 변환
    data["날짜"] = pd.to_datetime(
        data["일시"].astype(str).str.strip(),
        format="%b-%y",
        errors="coerce"
    )

    # 날짜가 정상적으로 변환되지 않은 행 제외
    data = data.dropna(subset=["날짜"]).copy()

    # 평균 기온 숫자로 변환
    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["평균기온(℃)"]
    ).copy()

    # 연도와 월 추출
    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    data["연도"] = data["연도"].astype(int)
    data["월"] = data["월"].astype(int)

    return data


# 파일 검색 및 불러오기
csv_path = find_csv_file()

if csv_path is None:

    st.error(
        "temperature.csv 파일을 찾을 수 없습니다."
    )

    st.info(
        "GitHub에서 temperature.csv 파일이 "
        "최상위 폴더 또는 pages 폴더와 같은 위치에 있는지 확인해주세요."
    )

    st.stop()


try:
    df = load_data(str(csv_path))

except Exception as e:
    st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
    st.stop()


st.success("기온 데이터 불러오기 성공!")

with st.expander("데이터 파일 정보 확인"):
    st.write("파일 위치:", str(csv_path))
    st.write("데이터 개수:", len(df))
    st.write("가장 오래된 연도:", df["연도"].min())
    st.write("가장 최근 연도:", df["연도"].max())


# ==========================================
# 4. 사용자 입력
# ==========================================
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

max_year = int(df["연도"].max())

st.subheader("📌 분석 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        options=list(month_names.keys()),
        format_func=lambda x: month_names[x]
    )

with col2:
    selected_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=max_year + 1,
        max_value=max_year + 100,
        value=max_year + 1,
        step=1
    )


# ==========================================
# 5. 선택한 월의 데이터 추출
# ==========================================
month_df = df[
    df["월"] == selected_month
].copy()

month_df = (
    month_df.groupby("연도", as_index=False)
    ["평균기온(℃)"]
    .mean()
    .sort_values("연도")
)

if len(month_df) < 2:
    st.warning(
        "선택한 월의 데이터가 2개 이상 있어야 예측할 수 있습니다."
    )
    st.stop()


# ==========================================
# 6. 선형회귀 알고리즘 학습
# ==========================================
X = month_df[["연도"]]
y = month_df["평균기온(℃)"]

model = LinearRegression()

# 과거 기온 데이터 학습
model.fit(X, y)

# 과거 데이터에 대한 회귀 예측
month_df["회귀예측기온"] = model.predict(X)

# 미래 연도 기온 예측
future_X = pd.DataFrame({
    "연도": [int(selected_year)]
})

predicted_temp = model.predict(future_X)[0]

# 결정계수
r2 = model.score(X, y)

# 기울기와 절편
slope = model.coef_[0]
intercept = model.intercept_


# ==========================================
# 7. 예측 결과 표시
# ==========================================
st.divider()

st.subheader(
    f"🌡️ {int(selected_year)}년 {month_names[selected_month]} 예측 결과"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{int(selected_year)}년"
    )

with col2:
    st.metric(
        "예측 평균 기온",
        f"{predicted_temp:.2f} ℃"
    )

with col3:
    st.metric(
        "결정계수 R²",
        f"{r2:.3f}"
    )


# ==========================================
# 8. 그래프 만들기
# ==========================================
st.divider()

st.subheader("📈 과거 기온과 미래 예측 시각화")

fig = go.Figure()

# 실제 평균 기온
fig.add_trace(
    go.Scatter(
        x=month_df["연도"],
        y=month_df["평균기온(℃)"],
        mode="markers",
        name="실제 평균 기온",
        marker=dict(
            color="#3498DB",
            size=9
        )
    )
)

# 회귀 직선을 부드럽게 그리기 위한 연도 생성
line_years = np.linspace(
    float(month_df["연도"].min()),
    float(selected_year),
    300
)

line_X = pd.DataFrame({
    "연도": line_years
})

line_y = model.predict(line_X)

# 선형회귀 직선
fig.add_trace(
    go.Scatter(
        x=line_years,
        y=line_y,
        mode="lines",
        name="선형회귀 직선",
        line=dict(
            color="#E74C3C",
            width=3
        )
    )
)

# 실제값과 회귀선의 차이
residual_x = []
residual_y = []

for _, row in month_df.iterrows():

    residual_x.extend([
        row["연도"],
        row["연도"],
        None
    ])

    residual_y.extend([
        row["회귀예측기온"],
        row["평균기온(℃)"],
        None
    ])

fig.add_trace(
    go.Scatter(
        x=residual_x,
        y=residual_y,
        mode="lines",
        name="예측 오차",
        line=dict(
            color="gray",
            width=1,
            dash="dot"
        ),
        hoverinfo="skip"
    )
)

# 미래 예측 기온
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[predicted_temp],
        mode="markers+text",
        name="미래 예측 기온",
        marker=dict(
            color="#F39C12",
            size=17,
            symbol="star"
        ),
        text=[f"{predicted_temp:.2f}℃"],
        textposition="top center"
    )
)

fig.update_layout(
    xaxis_title="연도",
    yaxis_title="평균 기온 (℃)",
    template="plotly_white",
    hovermode="x unified",
    height=550,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 9. 선형회귀 알고리즘 설명
# ==========================================
st.divider()

st.subheader("🧠 선형회귀 알고리즘 작동 원리")

st.markdown("### ① 선형회귀가 찾은 직선")

st.latex(
    rf"y = {slope:.4f}x + {intercept:.2f}"
)

st.write(
    f"기울기: {slope:.4f}"
)

st.write(
    f"절편: {intercept:.2f}"
)

st.write(
    f"결정계수(R²): {r2:.4f}"
)

st.markdown("### ② 선형회귀는 어떻게 작동할까요?")

st.markdown("""
선형회귀는 과거 데이터를 분석하여
실제 데이터에 가장 잘 맞는 직선을 찾는 알고리즘입니다.

**1단계. 데이터 수집**

선택한 월의 과거 평균 기온을 모읍니다.

**2단계. 데이터 학습**

연도와 평균 기온 사이의 관계를 분석합니다.

**3단계. 최적의 직선 찾기**

실제 기온과 직선이 예측한 기온의 차이를
제곱하여 모두 더한 값이 최소가 되도록 직선을 찾습니다.

**4단계. 미래 기온 예측**

학습한 직선에 사용자가 입력한 미래 연도를 넣어
예상 평균 기온을 계산합니다.
""")

st.markdown("### ③ 그래프 색깔 이해하기")

st.markdown("""
- 🔵 파란색 점: 실제로 측정한 과거 평균 기온
- 🔴 빨간색 선: 선형회귀가 학습한 추세선
- 🟠 주황색 별: 미래의 예측 평균 기온
- 회색 점선: 실제 기온과 회귀선 사이의 차이(오차)
""")

st.info(
    "결정계수 R²는 과거 데이터의 변동을 모델이 "
    "얼마나 설명하는지 나타냅니다. "
    "값이 1에 가까울수록 과거 데이터에 잘 맞지만 "
    "미래 예측의 정확성을 보장하지는 않습니다."
)


# ==========================================
# 10. 과거 기온 데이터 표
# ==========================================
st.divider()

st.subheader(
    f"📋 {month_names[selected_month]} 과거 기온 전체 데이터"
)

display_df = month_df[
    ["연도", "평균기온(℃)", "회귀예측기온"]
].copy()

display_df.columns = [
    "연도",
    "실제 평균 기온(℃)",
    "회귀선 예측 기온(℃)"
]

display_df = display_df.round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 11. 최종 예측 결과
# ==========================================
st.divider()

st.subheader("📝 최종 예측")

st.success(
    f"{int(selected_year)}년 {month_names[selected_month]}의 "
    f"예상 평균 기온은 {predicted_temp:.2f}℃입니다."
)

st.caption(
    "※ 과거 기온 데이터를 이용한 선형회귀 통계 예측이며, "
    "실제 기상 관측값이나 공식 기상 예보와 다를 수 있습니다."
)
