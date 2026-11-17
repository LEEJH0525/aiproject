
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from pathlib import Path


# --------------------------------------------------
# 1. 페이지 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write("선형회귀 알고리즘을 이용하여 선택한 월의 미래 평균기온을 예측합니다.")

st.divider()


# --------------------------------------------------
# 2. CSV 파일 찾기
# --------------------------------------------------

def find_csv_file():

    current_folder = Path(__file__).resolve().parent

    possible_paths = [
        current_folder / "temperature.csv",
        current_folder.parent / "temperature.csv",
        current_folder / "temperature (2).csv",
        current_folder.parent / "temperature (2).csv",
        current_folder / "tempre.csv",
        current_folder.parent / "tempre.csv",
        current_folder / "tempre (2).csv",
        current_folder.parent / "tempre (2).csv"
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


# --------------------------------------------------
# 3. CSV 데이터 불러오기
# --------------------------------------------------

@st.cache_data
def load_data(file_path):

    encodings = ["cp949", "utf-8-sig", "euc-kr", "utf-8"]

    for encoding in encodings:

        try:
            data = pd.read_csv(file_path, encoding=encoding)
            return data

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일의 인코딩을 읽을 수 없습니다.")


csv_path = find_csv_file()

if csv_path is None:

    st.error(
        "temperature.csv 파일을 찾을 수 없습니다. "
        "app.py와 같은 상위 폴더에 CSV 파일을 넣어 주세요."
    )

    st.stop()


try:
    df = load_data(str(csv_path))

except Exception as e:

    st.error(f"CSV 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------------------------
# 4. 날짜와 평균기온 데이터 정리
# --------------------------------------------------

if "일시" not in df.columns or "평균기온(℃)" not in df.columns:

    st.error(
        "CSV 파일에 '일시' 또는 '평균기온(℃)' 열이 없습니다."
    )

    st.stop()


# 날짜 변환
df["날짜"] = pd.to_datetime(
    df["일시"],
    format="%b-%y",
    errors="coerce"
)

# 평균기온 숫자 변환
df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

# 날짜 또는 기온이 없는 행 제거
df = df.dropna(
    subset=["날짜", "평균기온(℃)"]
).copy()

# 연도와 월 추출
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month


# --------------------------------------------------
# 5. 실제 데이터는 2025년까지만 사용
# --------------------------------------------------

df = df[df["연도"] <= 2025].copy()

df = df.sort_values("날짜")


if df.empty:
    st.error("2025년까지의 실제 기온 데이터가 없습니다.")
    st.stop()


# --------------------------------------------------
# 6. 사용자 입력
# --------------------------------------------------

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:

    selected_month = st.selectbox(
        "예측하고 싶은 월을 선택하세요.",
        options=list(range(1, 13)),
        format_func=lambda x: f"{x}월",
        index=0
    )


with col2:

    selected_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=2026,
        max_value=2125,
        value=2026,
        step=1
    )


# --------------------------------------------------
# 7. 선택한 월의 데이터 추출
# --------------------------------------------------

month_df = df[df["월"] == selected_month].copy()

month_df = month_df.sort_values("연도")


if len(month_df) < 2:

    st.warning(
        f"{selected_month}월의 데이터가 부족하여 "
        "선형회귀 예측을 진행할 수 없습니다."
    )

    st.stop()


# 독립변수 X: 연도
# 종속변수 y: 평균기온

X = month_df[["연도"]]
y = month_df["평균기온(℃)"]


# --------------------------------------------------
# 8. 선형회귀 모델 학습
# --------------------------------------------------

model = LinearRegression()

model.fit(X, y)


# 선택한 연도의 기온 예측
prediction = model.predict(
    pd.DataFrame({"연도": [int(selected_year)]})
)[0]


# 회귀식 정보
slope = model.coef_[0]
intercept = model.intercept_

r2 = model.score(X, y)


# --------------------------------------------------
# 9. 그래프를 위한 회귀선 데이터
# --------------------------------------------------

start_year = int(month_df["연도"].min())

graph_years = np.linspace(
    start_year,
    int(selected_year),
    200
)

graph_X = pd.DataFrame({
    "연도": graph_years
})

graph_predictions = model.predict(graph_X)


# --------------------------------------------------
# 10. 예측 결과 출력
# --------------------------------------------------

st.divider()

st.subheader("🔮 기온 예측 결과")

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:

    st.metric(
        label="선택한 월",
        value=f"{selected_month}월"
    )


with result_col2:

    st.metric(
        label="예측 연도",
        value=f"{int(selected_year)}년"
    )


with result_col3:

    st.metric(
        label="예측 평균기온",
        value=f"{prediction:.2f}℃"
    )


# --------------------------------------------------
# 11. 실제 데이터와 예측 그래프
# --------------------------------------------------

st.subheader(
    f"📈 {selected_month}월 실제 평균기온 및 미래 예측 그래프"
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
            color="royalblue",
            size=9
        )
    )
)


# 선형회귀 추세선
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=graph_predictions,
        mode="lines",
        name="선형회귀 추세선",
        line=dict(
            color="red",
            width=3
        )
    )
)


# 예측 기온
fig.add_trace(
    go.Scatter(
        x=[int(selected_year)],
        y=[prediction],
        mode="markers",
        name="예측 평균기온",
        marker=dict(
            color="orange",
            size=17,
            symbol="star"
        )
    )
)


# 예측값 설명 표시
fig.add_annotation(
    x=int(selected_year),
    y=prediction,
    text=f"예측: {prediction:.2f}℃",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)


fig.update_layout(
    title=f"{selected_month}월 평균기온 선형회귀 예측",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
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


# --------------------------------------------------
# 12. 선형회귀 알고리즘 설명
# --------------------------------------------------

st.divider()

st.subheader("🧠 선형회귀 알고리즘은 어떻게 작동할까요?")

st.write(
    "선형회귀는 과거의 연도와 평균기온 사이의 관계를 분석하여 "
    "가장 적합한 직선을 찾는 머신러닝 알고리즘입니다."
)

st.markdown("### ① 실제 데이터 확인")

st.write(
    f"{selected_month}월의 과거 평균기온 "
    "데이터를 이용합니다."
)

st.write(
    "그래프에서 파란색 점 하나하나가 실제 관측된 평균기온입니다."
)


st.markdown("### ② 가장 적합한 직선 찾기")

st.write(
    "선형회귀는 실제 데이터와 직선 사이의 오차가 "
    "전체적으로 작아지도록 직선을 계산합니다."
)

st.latex(r"y = ax + b")

st.write("각 기호의 의미는 다음과 같습니다.")

st.write(f"- **x** : 연도")
st.write(f"- **y** : 예측 평균기온")
st.write(f"- **a** : 기울기 ({slope:.4f})")
st.write(f"- **b** : 절편 ({intercept:.4f})")


st.markdown("### ③ 미래 기온 예측")

st.write(
    f"찾아낸 직선에 {int(selected_year)}년을 대입하면 "
    f"{selected_month}월의 평균기온을 예측할 수 있습니다."
)

st.latex(
    rf"y = {slope:.4f} \times {int(selected_year)} + ({intercept:.4f})"
)

st.success(
    f"{int(selected_year)}년 {selected_month}월의 "
    f"예측 평균기온은 {prediction:.2f}℃입니다."
)


# --------------------------------------------------
# 13. 결정계수 설명
# --------------------------------------------------

st.markdown("### ④ 모델의 설명력 확인")

st.write(
    f"결정계수 R² 값은 **{r2:.4f}**입니다."
)

st.write(
    "R²는 모델이 실제 데이터의 변화 정도를 "
    "얼마나 설명하는지 나타내는 지표입니다."
)

st.caption(
    "R²가 높다고 미래 예측이 반드시 정확하다는 뜻은 아닙니다. "
    "특히 먼 미래를 예측할수록 실제 기온과 차이가 커질 수 있습니다."
)


# --------------------------------------------------
# 14. 실제 데이터 표
# --------------------------------------------------

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


# --------------------------------------------------
# 15. 하단 안내
# --------------------------------------------------

st.divider()

st.caption(
    "※ 실제 데이터는 2025년까지만 사용합니다. "
    "2026년 이후의 값은 선형회귀 모델을 이용한 예측값입니다."
)
