
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")

st.write(
    "선형회귀, 2차 다항회귀, 3차 다항회귀를 이용하여 "
    "미래의 월별 평균기온을 예측합니다."
)

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
            return pd.read_csv(
                file_path,
                encoding=encoding
            )

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일 인코딩을 확인해 주세요.")


csv_path = find_csv_file()

if csv_path is None:

    st.error("temperature.csv 파일을 찾을 수 없습니다.")

    st.info(
        "CSV 파일을 app.py와 같은 상위 폴더에 넣어 주세요."
    )

    st.stop()


try:

    df = load_data(str(csv_path))

except Exception as e:

    st.error(f"CSV 파일 오류: {e}")
    st.stop()


# ==========================================
# 4. 데이터 정리
# ==========================================

if "일시" not in df.columns or "평균기온(℃)" not in df.columns:

    st.error(
        "CSV 파일에 '일시' 또는 '평균기온(℃)' 열이 없습니다."
    )

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
# 6. 알고리즘 선택
# ==========================================

st.subheader("🤖 회귀 알고리즘 선택")

algorithm_options = [
    "선형회귀",
    "2차 다항회귀",
    "3차 다항회귀"
]

selected_algorithm = st.radio(
    "사용할 알고리즘을 선택하세요.",
    algorithm_options,
    horizontal=True
)


# ==========================================
# 7. 선택한 월의 데이터 추출
# ==========================================

month_df = df[
    df["월"] == selected_month
].copy()

month_df = month_df.sort_values("연도")


if len(month_df) < 4:

    st.warning(
        "선택한 월의 데이터가 부족합니다. "
        "3차 다항회귀를 위해 최소 4개 이상의 연도 데이터가 필요합니다."
    )

    st.stop()


# 연도를 기준으로 학습
# 연도 값을 기준 연도에서 빼서 큰 숫자 계산으로 인한 불안정성을 줄임

base_year = int(month_df["연도"].min())

X = (
    month_df[["연도"]].astype(float) - base_year
)

y = month_df["평균기온(℃)"]


# ==========================================
# 8. 선형회귀 모델
# ==========================================

linear_model = LinearRegression()

linear_model.fit(X, y)


# ==========================================
# 9. 2차 다항회귀 모델
# ==========================================

polynomial2_model = make_pipeline(
    PolynomialFeatures(
        degree=2,
        include_bias=False
    ),
    LinearRegression()
)

polynomial2_model.fit(X, y)


# ==========================================
# 10. 3차 다항회귀 모델
# ==========================================

polynomial3_model = make_pipeline(
    PolynomialFeatures(
        degree=3,
        include_bias=False
    ),
    LinearRegression()
)

polynomial3_model.fit(X, y)


# ==========================================
# 11. 미래 연도 예측
# ==========================================

future_X = pd.DataFrame({
    "연도": [int(selected_year) - base_year]
})


linear_prediction = linear_model.predict(
    future_X
)[0]


polynomial2_prediction = polynomial2_model.predict(
    future_X
)[0]


polynomial3_prediction = polynomial3_model.predict(
    future_X
)[0]


# ==========================================
# 12. 모델 결정계수 계산
# ==========================================

linear_r2 = r2_score(
    y,
    linear_model.predict(X)
)

polynomial2_r2 = r2_score(
    y,
    polynomial2_model.predict(X)
)

polynomial3_r2 = r2_score(
    y,
    polynomial3_model.predict(X)
)


# ==========================================
# 13. 선택한 알고리즘 결과
# ==========================================

prediction_dict = {
    "선형회귀": linear_prediction,
    "2차 다항회귀": polynomial2_prediction,
    "3차 다항회귀": polynomial3_prediction
}

r2_dict = {
    "선형회귀": linear_r2,
    "2차 다항회귀": polynomial2_r2,
    "3차 다항회귀": polynomial3_r2
}

selected_prediction = prediction_dict[selected_algorithm]

selected_r2 = r2_dict[selected_algorithm]


# ==========================================
# 14. 그래프용 데이터 생성
# ==========================================

start_year = int(month_df["연도"].min())

graph_years = np.linspace(
    start_year,
    int(selected_year),
    300
)

graph_X = pd.DataFrame({
    "연도": graph_years - base_year
})


linear_graph = linear_model.predict(graph_X)

polynomial2_graph = polynomial2_model.predict(graph_X)

polynomial3_graph = polynomial3_model.predict(graph_X)


# ==========================================
# 15. 예측 결과 출력
# ==========================================

st.divider()

st.subheader("🔮 선택한 알고리즘의 예측 결과")

result1, result2, result3 = st.columns(3)

with result1:

    st.metric(
        "선택한 월",
        f"{selected_month}월"
    )

with result2:

    st.metric(
        "예측 연도",
        f"{int(selected_year)}년"
    )

with result3:

    st.metric(
        "선택한 알고리즘",
        selected_algorithm
    )


st.success(
    f"{selected_algorithm} 예측 평균기온은 "
    f"{selected_prediction:.2f}℃입니다."
)


# ==========================================
# 16. 세 가지 예측 결과 비교
# ==========================================

st.subheader("📊 세 가지 알고리즘 예측값 비교")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🔴 선형회귀",
        f"{linear_prediction:.2f}℃"
    )

with col2:

    st.metric(
        "🟢 2차 다항회귀",
        f"{polynomial2_prediction:.2f}℃"
    )

with col3:

    st.metric(
        "🟣 3차 다항회귀",
        f"{polynomial3_prediction:.2f}℃"
    )


# ==========================================
# 17. 그래프 표시
# ==========================================

st.divider()

st.subheader(
    f"📈 {selected_month}월 평균기온 예측 그래프"
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


# 2차 다항회귀
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=polynomial2_graph,
        mode="lines",
        name="2차 다항회귀",
        line=dict(
            color="green",
            width=3
        )
    )
)


# 3차 다항회귀
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=polynomial3_graph,
        mode="lines",
        name="3차 다항회귀",
        line=dict(
            color="purple",
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
            size=14,
            symbol="star"
        )
    )
)


# 2차 다항회귀 예측 위치
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[polynomial2_prediction],
        mode="markers",
        name="2차 다항회귀 예측값",
        marker=dict(
            color="green",
            size=14,
            symbol="star"
        )
    )
)


# 3차 다항회귀 예측 위치
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[polynomial3_prediction],
        mode="markers",
        name="3차 다항회귀 예측값",
        marker=dict(
            color="purple",
            size=14,
            symbol="star"
        )
    )
)


fig.update_layout(
    title=f"{selected_month}월 실제 기온 및 세 가지 회귀 예측 비교",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
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
# 18. 알고리즘 설명
# ==========================================

st.divider()

st.subheader("🧠 회귀 알고리즘 설명")


# 선형회귀
st.markdown("### 🔴 ① 선형회귀")

st.write(
    "선형회귀는 과거 연도와 평균기온 사이의 관계를 분석하여 "
    "가장 잘 맞는 직선을 찾는 알고리즘입니다."
)

st.latex(r"y = ax + b")

st.write(
    f"선형회귀 예측값: {linear_prediction:.2f}℃"
)


# 2차 다항회귀
st.markdown("### 🟢 ② 2차 다항회귀")

st.write(
    "2차 다항회귀는 2차식으로 곡선을 만들어 "
    "기온의 변화 추세를 표현합니다."
)

st.latex(r"y = ax^2 + bx + c")

st.write(
    f"2차 다항회귀 예측값: {polynomial2_prediction:.2f}℃"
)


# 3차 다항회귀
st.markdown("### 🟣 ③ 3차 다항회귀")

st.write(
    "3차 다항회귀는 3차식을 이용하여 "
    "더 다양한 곡선 형태의 변화 추세를 표현할 수 있습니다."
)

st.latex(r"y = ax^3 + bx^2 + cx + d")

st.write(
    f"3차 다항회귀 예측값: {polynomial3_prediction:.2f}℃"
)


# ==========================================
# 19. 선택한 알고리즘 안내
# ==========================================

st.divider()

st.subheader("🎯 선택한 알고리즘 정보")

if selected_algorithm == "선형회귀":

    st.info(
        "선형회귀를 선택했습니다. "
        "과거 데이터의 직선적인 변화 추세를 이용합니다."
    )

elif selected_algorithm == "2차 다항회귀":

    st.info(
        "2차 다항회귀를 선택했습니다. "
        "과거 데이터의 2차 곡선 변화 추세를 이용합니다."
    )

else:

    st.info(
        "3차 다항회귀를 선택했습니다. "
        "과거 데이터의 3차 곡선 변화 추세를 이용합니다."
    )


st.write(
    f"선택한 모델의 학습 데이터 R² 값: {selected_r2:.4f}"
)

st.caption(
    "R²는 학습 데이터에 대한 설명력입니다. "
    "차수가 높을수록 학습 데이터에 더 잘 맞을 수 있지만, "
    "미래 예측이 반드시 더 정확해지는 것은 아닙니다."
)


# ==========================================
# 20. 실제 기온 데이터 표
# ==========================================

st.divider()

st.subheader("📋 학습에 사용된 실제 기온 데이터")

display_df = month_df[
    ["연도", "월", "평균기온(℃)"]
].copy()

display_df["월"] = (
    display_df["월"].astype(str) + "월"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 21. 안내 문구
# ==========================================

st.divider()

st.caption(
    "※ 실제 기온 데이터는 2025년까지만 사용합니다. "
    "2026년 이후의 값은 세 가지 회귀 알고리즘으로 계산한 예측값입니다."
)
