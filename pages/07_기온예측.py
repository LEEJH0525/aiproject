
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path
import re

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="월평균 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월평균 기온 분석 및 예측")
st.markdown(
    "과거 기온 데이터를 분석하고 **선형회귀 알고리즘**으로 "
    "미래의 월평균 기온을 예측합니다."
)

st.divider()


# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():

    file_path = Path(__file__).resolve().parent / "temperature(2).csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "temperature.csv 파일을 app.py와 같은 폴더에 넣어주세요."
        )

    # 한글 CSV 인코딩 대응
    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(file_path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            data = pd.read_csv(file_path, encoding="euc-kr")

    required_columns = ["일시", "평균기온(℃)"]

    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"CSV에 '{col}' 컬럼이 없습니다.")

    data = data.copy()

    # 날짜 형식: Oct-07, Nov-07 등
    # 파일의 순서에 따라 두 자리 연도를 복원
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3,
        "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12
    }

    years = []
    months = []
    century = 1900
    previous_yy = None

    for value in data["일시"]:

        match = re.fullmatch(
            r"\s*([A-Za-z]{3})-(\d{2})\s*",
            str(value)
        )

        if not match:
            years.append(np.nan)
            months.append(np.nan)
            continue

        month_name = match.group(1).title()
        yy = int(match.group(2))

        if month_name not in month_map:
            years.append(np.nan)
            months.append(np.nan)
            continue

        # 연도가 99에서 00으로 넘어가는 경우 세기 변경
        if previous_yy is not None and yy < previous_yy:
            century += 100

        year = century + yy

        years.append(year)
        months.append(month_map[month_name])
        previous_yy = yy

    data["연도"] = years
    data["월"] = months

    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    )

    data["연도"] = data["연도"].astype(int)
    data["월"] = data["월"].astype(int)

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------
# 3. 사용자 입력
# --------------------------------
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        options=list(month_names.keys()),
        format_func=lambda x: month_names[x],
        index=0
    )

with col2:
    selected_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=max_year + 1,
        max_value=max_year + 100,
        value=max_year + 1,
        step=1
    )

st.divider()


# --------------------------------
# 4. 선택한 월 데이터 추출
# --------------------------------
month_df = df[df["월"] == selected_month].copy()

if len(month_df) < 2:
    st.warning("선택한 월의 데이터가 2개 이상 필요합니다.")
    st.stop()

# 같은 연도에 중복된 자료가 있다면 평균으로 통합
month_df = (
    month_df.groupby("연도", as_index=False)
    ["평균기온(℃)"].mean()
    .sort_values("연도")
)

X = month_df[["연도"]]
y = month_df["평균기온(℃)"]

if len(month_df) < 2:
    st.warning("선형회귀를 학습할 데이터가 부족합니다.")
    st.stop()


# --------------------------------
# 5. 선형회귀 학습
# --------------------------------
model = LinearRegression()

model.fit(X, y)

# 과거 데이터 예측값
month_df["회귀예측기온"] = model.predict(X)

# 미래 기온 예측
future_X = pd.DataFrame({
    "연도": [int(selected_year)]
})

predicted_temp = model.predict(future_X)[0]

# 회귀식 정보
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)


# --------------------------------
# 6. 예측 결과 표시
# --------------------------------
st.subheader(
    f"🌡️ {month_names[selected_month]} 평균 기온 예측 결과"
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
        "결정계수 (R²)",
        f"{r2:.3f}"
    )

st.divider()


# --------------------------------
# 7. 그래프 생성
# --------------------------------
st.subheader("📈 과거 기온과 미래 예측 그래프")

fig = go.Figure()

# 과거 실제 기온
fig.add_trace(go.Scatter(
    x=month_df["연도"],
    y=month_df["평균기온(℃)"],
    mode="markers",
    name="실제 평균 기온",
    marker=dict(
        color="#3498DB",
        size=9
    )
))

# 회귀 직선
line_years = np.linspace(
    min_year,
    int(selected_year),
    300
)

line_X = pd.DataFrame({
    "연도": line_years
})

line_y = model.predict(line_X)

fig.add_trace(go.Scatter(
    x=line_years,
    y=line_y,
    mode="lines",
    name="선형회귀 직선",
    line=dict(
        color="#E74C3C",
        width=3
    )
))

# 실제 데이터와 회귀선 사이의 오차 표시
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

fig.add_trace(go.Scatter(
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
))

# 미래 예측 지점
fig.add_trace(go.Scatter(
    x=[int(selected_year)],
    y=[predicted_temp],
    mode="markers+text",
    name="미래 예측 기온",
    marker=dict(
        color="#F39C12",
        size=16,
        symbol="star"
    ),
    text=[f"{predicted_temp:.2f}℃"],
    textposition="top center"
))

fig.update_layout(
    xaxis_title="연도",
    yaxis_title="평균 기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
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


# --------------------------------
# 8. 선형회귀 알고리즘 정보
# --------------------------------
st.subheader("🧠 선형회귀 알고리즘 작동 원리")

st.markdown("### ① 학습된 회귀식")

st.latex(
    r"y = {:.4f}x + {:.2f}".format(slope, intercept)
)

st.write(
    f"- 기울기: {slope:.4f}"
)

st.write(
    f"- 절편: {intercept:.2f}"
)

st.write(
    f"- 결정계수(R²): {r2:.4f}"
)

st.markdown("### ② 선형회귀는 어떻게 작동할까요?")

st.markdown("""
선형회귀는 과거의 데이터를 이용하여
가장 잘 맞는 직선을 찾는 머신러닝 알고리즘입니다.

이번 프로그램에서는 다음과 같이 작동합니다.

1. **데이터 수집:** 선택한 월의 과거 평균 기온을 모읍니다.
2. **학습:** 각 연도와 평균 기온 사이의 관계를 분석합니다.
3. **직선 찾기:** 실제 기온과 직선 사이의 오차 제곱 합이
   가장 작아지는 직선을 찾습니다.
4. **예측:** 학습한 직선에 사용자가 입력한 미래 연도를 넣어
   예상 평균 기온을 계산합니다.
""")

st.markdown("### ③ 그래프에서 확인할 수 있는 것")

st.markdown("""
- 🔵 **파란 점:** 실제로 관측된 과거 평균 기온입니다.
- 🔴 **빨간 선:** 선형회귀 알고리즘이 찾은 최적의 직선입니다.
- 🟠 **주황색 별:** 입력한 연도의 예측 기온입니다.
- 회색 점선: 실제 기온과 회귀 직선 사이의 예측 오차입니다.
""")

st.info(
    "결정계수(R²)는 회귀 모델이 과거 기온 데이터의 "
    "변동을 얼마나 설명하는지 나타냅니다. "
    "1에 가까울수록 과거 데이터에 잘 맞지만, "
    "미래 예측이 반드시 정확하다는 의미는 아닙니다."
)


# --------------------------------
# 9. 과거 데이터 표
# --------------------------------
st.subheader("📋 선택한 월의 과거 기온 데이터")

display_df = month_df[
    ["연도", "평균기온(℃)", "회귀예측기온"]
].copy()

display_df.columns = [
    "연도",
    "실제 평균 기온(℃)",
    "회귀선 기온(℃)"
]

st.dataframe(
    display_df.sort_values("연도"),
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# 10. 예측 결과 정리
# --------------------------------
st.subheader("📝 최종 예측 결과")

st.success(
    f"{int(selected_year)}년 {month_names[selected_month]}의 "
    f"예상 평균 기온은 {predicted_temp:.2f}℃입니다."
)

st.caption(
    "※ 이 결과는 과거 데이터에 선형회귀 모델을 적용한 통계적 예측값이며, "
    "실제 기상 예보와 다를 수 있습니다."
)
