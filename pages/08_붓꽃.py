
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하여 붓꽃의 품종을 예측해 보세요.")

st.divider()

# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():

    current_folder = Path(__file__).resolve().parent

    possible_paths = [
        current_folder / "Iris.csv",
        current_folder.parent / "Iris.csv"
    ]

    file_path = None

    for path in possible_paths:
        if path.exists():
            file_path = path
            break

    if file_path is None:
        raise FileNotFoundError(
            "Iris.csv 파일을 프로젝트 폴더 또는 상위 폴더에 넣어주세요."
        )

    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    data.columns = data.columns.str.strip()

    required = ["꽃잎 길이", "꽃잎 너비", "품종"]

    for col in required:
        if col not in data.columns:
            raise ValueError(f"'{col}' 컬럼이 CSV에 없습니다.")

    data = data.dropna(subset=required).copy()

    data["품종"] = (
        data["품종"].astype(str)
        .str.strip()
        .str.replace("Iris-", "", regex=False)
    )

    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()

# --------------------------------
# 3. 데이터 준비
# --------------------------------
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

length_min = float(df["꽃잎 길이"].min())
length_max = float(df["꽃잎 길이"].max())

width_min = float(df["꽃잎 너비"].min())
width_max = float(df["꽃잎 너비"].max())

# --------------------------------
# 4. 학습 데이터와 테스트 데이터 분리
# --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------
# 5. 랜덤 포레스트 알고리즘
# --------------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 모델 학습
model.fit(X_train, y_train)

# 정확도 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# 전체 데이터로 최종 학습
model.fit(X, y)

# --------------------------------
# 6. 데이터 정보
# --------------------------------
st.subheader("📊 데이터 분석")

col1, col2, col3 = st.columns(3)

col1.metric("전체 데이터", f"{len(df)}개")
col2.metric("붓꽃 품종", f"{y.nunique()}종")
col3.metric("모델 정확도", f"{accuracy * 100:.1f}%")

st.divider()

# --------------------------------
# 7. 사용 알고리즘 설명
# --------------------------------
st.subheader("🤖 예측에 사용한 알고리즘")

st.success("사용 알고리즘: 랜덤 포레스트 (Random Forest)")

st.markdown("""
### 🌳 랜덤 포레스트란?

랜덤 포레스트는 여러 개의 의사결정나무를 만들어
각각 예측한 결과를 모아서 최종 결과를 결정하는
머신러닝 분류 알고리즘입니다.

쉽게 말하면 여러 명이 함께 의견을 내고
가장 많은 표를 받은 답을 선택하는 방법입니다.
""")

st.markdown("### 🔍 작동 과정")

st.markdown("""
**1단계. 데이터 학습**

기존 Iris.csv에 있는 꽃잎 길이와 꽃잎 너비,
붓꽃 품종 데이터를 학습합니다.

**2단계. 여러 개의 의사결정나무 생성**

서로 다른 학습 데이터와 특성 조합을 이용하여
100개의 의사결정나무를 만듭니다.

**3단계. 각각 품종 예측**

각각의 나무가 입력된 꽃잎 길이와 너비를 보고
Setosa, Versicolor, Virginica 중 하나를 예측합니다.

**4단계. 다수결 투표**

100개의 나무가 예측한 결과를 모아서
가장 많은 표를 받은 품종을 선택합니다.

**5단계. 최종 품종 결정**

가장 많은 표를 받은 붓꽃 품종을
최종 예측 결과로 보여줍니다.
""")

st.info(
    "이 프로그램은 100개의 의사결정나무를 사용하는 "
    "랜덤 포레스트 분류 모델입니다."
)

with st.expander("📚 랜덤 포레스트의 장점과 특징"):

    st.write("""
    - 여러 의사결정나무를 사용하여 예측합니다.
    - 하나의 나무보다 다양한 판단을 활용할 수 있습니다.
    - 분류와 예측 문제에 사용할 수 있습니다.
    - 여러 나무의 예측 확률을 종합하여 품종별 확률을 계산합니다.
    """)

st.divider()

# --------------------------------
# 8. 사용자 입력
# --------------------------------
st.subheader("✏️ 꽃잎 크기 입력")

st.info(f"""
**입력 가능한 값의 범위**

- 꽃잎 길이: {length_min} ~ {length_max} cm
- 꽃잎 너비: {width_min} ~ {width_max} cm

CSV 데이터의 실제 최솟값과 최댓값을 기준으로 합니다.
""")

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=length_min,
        max_value=length_max,
        value=3.8,
        step=0.1
    )

with col2:
    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=width_min,
        max_value=width_max,
        value=1.2,
        step=0.1
    )

# --------------------------------
# 9. 품종 예측
# --------------------------------
if st.button("🌸 붓꽃 품종 예측하기", type="primary"):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    st.success(f"🌸 예측 결과: {prediction}")

    st.subheader("🔍 품종별 예측 확률")

    prob_df = pd.DataFrame({
        "품종": model.classes_,
        "예측 확률": probabilities * 100
    })

    fig_prob = px.bar(
        prob_df,
        x="품종",
        y="예측 확률",
        color="품종",
        text_auto=".1f",
        title="품종별 예측 확률"
    )

    fig_prob.update_layout(
        yaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_prob, use_container_width=True)

    st.caption(
        "예측 확률은 랜덤 포레스트에 포함된 여러 나무의 "
        "품종별 예측 확률을 종합한 값입니다."
    )

# --------------------------------
# 10. 산점도 그래프
# --------------------------------
st.divider()

st.subheader("📈 꽃잎 길이와 꽃잎 너비 비교")

st.write(
    "가로축은 꽃잎 길이, 세로축은 꽃잎 너비입니다. "
    "노란색 별은 사용자가 입력한 위치입니다."
)

fig = px.scatter(
    df,
    x="꽃잎 길이",
    y="꽃잎 너비",
    color="품종",
    title="붓꽃 품종별 꽃잎 크기",
    color_discrete_map={
        "setosa": "#3498DB",
        "versicolor": "#2ECC71",
        "virginica": "#E74C3C"
    }
)

fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],
        mode="markers",
        name="사용자 입력 위치",
        marker=dict(
            symbol="star",
            size=25,
            color="yellow",
            line=dict(color="black", width=2)
        )
    )
)

fig.update_layout(
    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# 11. 원본 데이터
# --------------------------------
with st.expander("📋 원본 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)

st.divider()

st.caption(
    "사용 알고리즘: Random Forest Classifier | "
    "학습 나무 개수: 100개"
)
