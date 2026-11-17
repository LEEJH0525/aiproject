
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write("선형회귀와 다항회귀를 이용한 미래 기온 예측")
st.divider()


# ==========================================
# 2. CSV 파일 찾기
# ==========================================

def find_csv_file():

    current_folder = Path(__file__).resolve().parent

    file_names = [
        "temperature.csv",
        "temperature (2).csv",
        "tempre.csv",
        "tempre (2).csv"
    ]

    for folder in [current_folder, current_folder.parent]:

        for file_name in file_names:

            file_path = folder / file_name

            if file_path.exists():
                return file_path

    return None


# ==========================================
# 3. CSV 데이터 불러오기
# ==========================================

@st.cache_data
def load_data(file_path):

    for encoding in ["cp949", "utf-8-sig", "euc-kr", "utf-8"]:

        try:
            return pd.read_csv(file_path, encoding=encoding)

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일 인코딩을 확인해 주세요.")


csv_path = find_csv_file()

if csv_path is None:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("CSV 파일을 app.py와 같은 상위 폴더에 넣어 주세요.")
    st.stop()

try:
    df = load_data(str(csv_path))

except Exception as e:
    st.error(f"CSV 파일을 불러오지 못했습니다: {e}")
    st.stop()


# ==========================================
# 4. 데이터 정리
# ==========================================

if "일시" not in df.columns or "평균기온(℃)" not in df.columns:
    st.error("CSV 파일에 '일시' 또는 '평균기온(℃)' 열이 없습니다.")
    st.stop()

df["날짜"] = pd.to_datetime(
    df["일시"],
    format="%b-%y",
    errors="coerce"
)

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

df = df.dropna(
    subset=["날짜", "평균기온(℃)"]
).copy()

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# 실제 데이터는 2025년까지만 사용
df = df[df["연도"] <= 2025].copy()

df = df.sort_values("날짜")

if df.empty:
    st.error("2025년까지의 실제 기온 데이터가 없습니다.")
    st.stop()


# ==========================================
# 5. 사용자 입력
# ==========================================

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "예측할 월",
        range(1, 13),
        format_func=lambda x: f"{x}월"
    )

with col2:
    selected_year = st.number_input(
        "예측할 연도",
        min_value=2026,
        max_value=2125,
        value=2026,
        step=1
    )


# ==========================================
# 6. 회귀 알고리즘 선택
# ==========================================

st.subheader("🤖 회귀 알고리즘 선택")

selected_algorithm = st.radio(
    "사용할 알고리즘을 선택하세요.",
    ["선형회귀", "다항회귀"],
    horizontal=True
)


# ==========================================
# 7. 선택한 월의 데이터 추출
# ==========================================

month_df = df[df["월"] == selected_month].copy()
month_df = month_df.sort_values("연도")

if len(month_df) < 3:
    st.warning("선택한 월의 데이터가 부족합니다. 3개 이상의 연도 데이터가 필요합니다.")
    st.stop()

X = month_df[["연도"]]
y = month_df["평균기온(℃)"]


# ==========================================
# 8. 선형회귀 모델
# ==========================================

linear_model = LinearRegression()
linear_model.fit(X, y)

future_X = pd.DataFrame({
    "연도": [int(selected_year)]
})

linear_prediction = linear_model.predict(future_X)[0]
linear_r2 = linear_model.score(X, y)


# ==========================================
# 9. 다항회귀 모델
# ==========================================

polynomial_model = make_pipeline(
    PolynomialFeatures(degree=2),
    LinearRegression()
)

polynomial_model.fit(X, y)

polynomial_prediction = polynomial_model.predict(future_X)[0]
polynomial_r2 = polynomial_model.score(X, y)


# ==========================================
# 10. 선택 알고리즘 결과
# ==========================================

if selected_algorithm == "선형회귀":

    selected_prediction = linear_prediction
    selected_r2 = linear_r2

else:

    selected_prediction = polynomial_prediction
    selected_r2 = polynomial_r2


# ==========================================
# 11. 그래프 데이터 생성
# ==========================================

start_year = int(month_df["연도"].min())

graph_years = np.linspace(
    start_year,
    int(selected_year),
    200
)

graph_X = pd.DataFrame({
    "연도": graph_years
})

linear_graph = linear_model.predict(graph_X)
polynomial_graph = polynomial_model.predict(graph_X)


# ==========================================
# 12. 예측 결과
# ==========================================

st.divider()
st.subheader("🔮 기온 예측 결과")

result1, result2, result3 = st.columns(3)

with result1:
    st.metric("선택한 월", f"{selected_month}월")

with result2:
    st.metric("예측 연도", f"{int(selected_year)}년")

with result3:
    st.metric("선택한 알고리즘", selected_algorithm)

st.success(
    f"{selected_algorithm} 예측 평균기온: {selected_prediction:.2f}℃"
)

st.markdown("### 두 알고리즘의 예측 결과 비교")

compare1, compare2 = st.columns(2)

with compare1:
    st.metric(
        "🔴 선형회귀 예측",
        f"{linear_prediction:.2f}℃"
    )

with compare2:
    st.metric(
        "🟢 다항회귀 예측",
        f"{polynomial_prediction:.2f}℃"
    )


# ==========================================
# 13. 세 가지 그래프 표시
# ==========================================

st.divider()

st.subheader(
    f"📈 {selected_month}월 평균기온 그래프 비교"
)

fig = go.Figure()

# 실제 평균기온
fig.add_trace(
    go.Scatter(
        x=month_df["연도"],
        y=month_df["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="blue",
            size=9
        )
    )
)

# 선형회귀
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=linear_graph,
        mode="lines",
        name="선형회귀",
        line=dict(
            color="red",
            width=3
        )
    )
)

# 다항회귀
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=polynomial_graph,
        mode="lines",
        name="다항회귀",
        line=dict(
            color="green",
            width=3
        )
    )
)

# 선형회귀 예측 위치
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[linear_prediction],
        mode="markers",
        name="선형회귀 예측값",
        marker=dict(
            color="red",
            size=15,
            symbol="star"
        )
    )
)

# 다항회귀 예측 위치
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[polynomial_prediction],
        mode="markers",
        name="다항회귀 예측값",
        marker=dict(
            color="green",
            size=15,
            symbol="star"
        )
    )
)

fig.update_layout(
    title=f"{selected_month}월 평균기온 예측 비교",
    xaxis_title="연도",
    yaxis_title="평균기온(℃)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 14. 알고리즘 설명
# ==========================================

st.divider()
st.subheader("🧠 회귀 알고리즘 설명")

# 선형회귀 설명
st.markdown("### 🔴 ① 선형회귀")

st.write(
    "선형회귀는 과거의 연도와 평균기온을 분석하여 "
    "데이터에 가장 잘 맞는 직선을 찾는 알고리즘입니다."
)

st.latex(r"y = ax + b")

st.write("""
- x: 연도
- y: 예측 평균기온
- a: 직선의 기울기
- b: y절편
""")

st.write(
    f"선형회귀 예측 결과: **{linear_prediction:.2f}℃**"
)


# 다항회귀 설명
st.markdown("### 🟢 ② 다항회귀")

st.write(
    "다항회귀는 직선이 아닌 곡선을 이용하여 "
    "데이터의 변화 추세를 나타낼 수 있는 알고리즘입니다."
)

st.latex(r"y = ax^2 + bx + c")

st.write(
    "이번 프로그램에서는 2차 다항회귀를 사용합니다. "
    "과거 기온의 변화가 곡선 형태로 나타나는 경우를 표현할 수 있습니다."
)

st.write(
    f"다항회귀 예측 결과: **{polynomial_prediction:.2f}℃**"
)


# ==========================================
# 15. 사용자가 선택한 알고리즘 설명
# ==========================================

st.divider()
st.subheader("🎯 내가 선택한 알고리즘")

if selected_algorithm == "선형회귀":

    st.info(
        "선형회귀를 선택했습니다. "
        "과거 기온 데이터의 직선적인 변화 추세를 이용합니다."
    )

else:

    st.info(
        "다항회귀를 선택했습니다. "
        "과거 기온 데이터의 곡선 형태 변화 추세를 이용합니다."
    )

st.write(f"선택한 알고리즘의 R² 값: **{selected_r2:.4f}**")

st.caption(
    "R²는 학습 데이터에 대한 설명력을 나타냅니다. "
    "값이 높더라도 미래 예측의 정확성을 보장하지는 않습니다."
)


# ==========================================
# 16. 실제 기온 데이터 표
# ==========================================

st.divider()
st.subheader("📋 학습에 사용된 실제 기온 데이터")

display_df = month_df[
    ["연도", "월", "평균기온(℃)"]
].copy()

display_df["월"] = display_df["월"].astype(str) + "월"

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 17. 안내 문구
# ==========================================

st.divider()

st.caption(
    "실제 기온 데이터는 2025년까지만 사용합니다. "
    "2026년 이후의 값은 회귀 알고리즘을 이용한 예측값입니다."
)
