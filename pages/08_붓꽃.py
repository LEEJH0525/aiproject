
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# ---------------------------------------
# 1. 페이지 설정
# ---------------------------------------
st.set_page_config(
    page_title="붓꽃 품종 예측 비교",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 및 알고리즘 비교")
st.write(
    "꽃잎 길이와 꽃잎 너비를 입력하면 "
    "3가지 머신러닝 알고리즘이 붓꽃 품종을 예측합니다."
)

st.divider()

# ---------------------------------------
# 2. CSV 파일 불러오기
# ---------------------------------------
@st.cache_data
def load_data():

    current_folder = Path(__file__).resolve().parent

    possible_paths = [
        current_folder / "Iris.csv",
        current_folder.parent / "Iris.csv",
        current_folder.parent.parent / "Iris.csv"
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

    # 컬럼명 공백 제거
    data.columns = data.columns.str.strip()

    required = ["꽃잎 길이", "꽃잎 너비", "품종"]

    for col in required:
        if col not in data.columns:
            raise ValueError(
                f"CSV 파일에 '{col}' 컬럼이 없습니다."
            )

    data = data.dropna(subset=required).copy()

    data["품종"] = (
        data["품종"].astype(str)
        .str.strip()
        .str.replace("Iris-", "", regex=False)
    )

    data["꽃잎 길이"] = pd.to_numeric(
        data["꽃잎 길이"], errors="coerce"
    )

    data["꽃잎 너비"] = pd.to_numeric(
        data["꽃잎 너비"], errors="coerce"
    )

    data = data.dropna(
        subset=["꽃잎 길이", "꽃잎 너비", "품종"]
    )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()

# ---------------------------------------
# 3. 데이터 준비
# ---------------------------------------
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

length_min = float(df["꽃잎 길이"].min())
length_max = float(df["꽃잎 길이"].max())

width_min = float(df["꽃잎 너비"].min())
width_max = float(df["꽃잎 너비"].max())

# ---------------------------------------
# 4. 학습 데이터와 테스트 데이터 분리
# ---------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------
# 5. 분류 알고리즘 3개 생성
# ---------------------------------------

# 알고리즘 1: 랜덤 포레스트
random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 알고리즘 2: K-최근접 이웃
knn = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

# 알고리즘 3: 로지스틱 회귀
logistic = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

# 알고리즘 저장
models = {
    "랜덤 포레스트": random_forest,
    "K-최근접 이웃": knn,
    "로지스틱 회귀": logistic
}

# ---------------------------------------
# 6. 모델 학습 및 정확도 평가
# ---------------------------------------
accuracies = {}

for name, model in models.items():

    model.fit(X_train, y_train)

    test_prediction = model.predict(X_test)

    accuracies[name] = accuracy_score(
        y_test,
        test_prediction
    )

# 전체 데이터로 최종 학습
for model in models.values():
    model.fit(X, y)

# ---------------------------------------
# 7. 데이터 정보
# ---------------------------------------
st.subheader("📊 붓꽃 데이터 정보")

c1, c2, c3 = st.columns(3)

c1.metric("전체 데이터", f"{len(df)}개")
c2.metric("붓꽃 품종", f"{y.nunique()}종")
c3.metric("사용 알고리즘", "3개")

st.divider()

# ---------------------------------------
# 8. 알고리즘 소개
# ---------------------------------------
st.subheader("🤖 예측에 사용하는 알고리즘")

st.write(
    "이번 프로그램은 서로 다른 3가지 분류 알고리즘을 "
    "사용하여 붓꽃 품종을 예측합니다."
)

with st.expander("① 랜덤 포레스트 (Random Forest) 작동 원리"):

    st.markdown("""
    ### 🌳 여러 나무가 투표하는 방법

    랜덤 포레스트는 여러 개의 의사결정나무를 만들어
    각각 예측한 결과를 종합하는 알고리즘입니다.

    **작동 과정**

    1. 기존 붓꽃 데이터를 학습합니다.
    2. 서로 다른 데이터와 특성을 활용하여 여러 의사결정나무를 만듭니다.
    3. 각각의 나무가 입력한 꽃잎 크기를 보고 품종을 예측합니다.
    4. 모든 나무의 예측 결과를 모읍니다.
    5. 가장 많은 표를 받은 품종을 최종 결과로 선택합니다.

    **쉽게 이해하기**

    여러 명이 문제를 풀고 다수결로 정답을 결정하는 것과 비슷합니다.

    **이번 프로그램 설정**

    - 의사결정나무 개수: 100개
    - 최종 결정 방법: 다수결
    """)

with st.expander("② K-최근접 이웃 (KNN) 작동 원리"):

    st.markdown("""
    ### 📍 가까운 이웃을 찾아서 예측하는 방법

    KNN은 새로운 데이터와 가까운 기존 데이터를 찾아
    가장 많은 품종을 선택하는 알고리즘입니다.

    **작동 과정**

    1. 기존 붓꽃 데이터를 저장합니다.
    2. 사용자가 꽃잎 길이와 너비를 입력합니다.
    3. 입력한 데이터와 기존 데이터 사이의 거리를 계산합니다.
    4. 가장 가까운 데이터 5개를 찾습니다.
    5. 5개 중 가장 많은 품종을 최종 결과로 선택합니다.

    **쉽게 이해하기**

    새로운 학생이 전학 왔을 때 가까운 친구 5명의 의견을 듣고
    가장 많은 의견을 선택하는 것과 비슷합니다.

    **이번 프로그램 설정**

    - 이웃 데이터 개수 K: 5개
    - 거리 계산 전 데이터 표준화 적용
    """)

with st.expander("③ 로지스틱 회귀 (Logistic Regression) 작동 원리"):

    st.markdown("""
    ### 📈 확률을 계산하여 예측하는 방법

    로지스틱 회귀는 입력된 데이터를 바탕으로
    각 품종에 속할 확률을 계산하는 분류 알고리즘입니다.

    **작동 과정**

    1. 기존 꽃잎 길이와 너비 데이터를 학습합니다.
    2. 꽃잎 길이와 너비의 관계를 분석합니다.
    3. 입력된 값이 각 품종에 속할 확률을 계산합니다.
    4. 세 품종의 예측 확률을 비교합니다.
    5. 가장 높은 확률을 가진 품종을 선택합니다.

    **쉽게 이해하기**

    세 가지 선택지 중 어떤 답이 가장 가능성이 높은지
    확률을 계산해서 선택하는 방법입니다.

    **이번 프로그램 설정**

    - 분류 방식: 다중 클래스 분류
    - 확률 계산: 소프트맥스 방식
    - 입력 데이터 표준화 적용
    """)

st.info(
    "세 알고리즘 모두 꽃잎 길이와 꽃잎 너비 두 가지 "
    "특성만 사용하여 학습합니다."
)

st.divider()

# ---------------------------------------
# 9. 사용자 입력
# ---------------------------------------
st.subheader("✏️ 꽃잎 크기 입력하기")

st.info(f"""
**입력 가능한 값의 범위**

- 꽃잎 길이: {length_min} ~ {length_max} cm
- 꽃잎 너비: {width_min} ~ {width_max} cm

※ 기존 Iris.csv 데이터의 실제 최솟값과 최댓값입니다.
""")

col1, col2 = st.columns(2)

with col1:

    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=length_min,
        max_value=length_max,
        value=3.8,
        step=0.1,
        format="%.1f"
    )

with col2:

    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=width_min,
        max_value=width_max,
        value=1.2,
        step=0.1,
        format="%.1f"
    )

# ---------------------------------------
# 10. 세 가지 알고리즘 예측
# ---------------------------------------
st.divider()

st.subheader("🔍 세 가지 알고리즘 예측 결과")

if st.button(
    "🌸 3가지 알고리즘으로 품종 예측하기",
    type="primary",
    use_container_width=True
):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    results = []
    probability_data = []

    for name, model in models.items():

        prediction = model.predict(input_data)[0]

        probabilities = model.predict_proba(input_data)[0]

        confidence = max(probabilities) * 100

        results.append({
            "알고리즘": name,
            "예측 품종": prediction,
            "예측 확률": confidence,
            "테스트 정확도": accuracies[name] * 100
        })

        for species, prob in zip(
            model.classes_,
            probabilities
        ):

            probability_data.append({
                "알고리즘": name,
                "품종": species,
                "예측 확률": prob * 100
            })

    result_df = pd.DataFrame(results)

    probability_df = pd.DataFrame(probability_data)

    # 예측 결과 표
    st.subheader("📋 알고리즘별 예측 비교")

    st.dataframe(
        result_df.style.format({
            "예측 확률": "{:.1f}%",
            "테스트 정확도": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # 알고리즘별 예측 품종
    st.subheader("🏆 알고리즘별 예측 품종")

    result_cols = st.columns(3)

    for i, row in result_df.iterrows():

        with result_cols[i]:

            st.markdown(f"**{row['알고리즘']}**")

            st.success(
                f"🌸 {row['예측 품종']}"
            )

            st.metric(
                "예측 확률",
                f"{row['예측 확률']:.1f}%"
            )

    # 세 알고리즘의 예측 일치 여부
    st.subheader("🤝 예측 결과 일치 여부")

    unique_predictions = result_df["예측 품종"].nunique()

    if unique_predictions == 1:

        st.success(
            "세 알고리즘 모두 같은 품종을 예측했습니다!"
        )

    else:

        st.warning(
            "알고리즘마다 예측 결과가 다릅니다. "
            "각 알고리즘의 판단 방식을 비교해 보세요."
        )

    # 품종별 확률 비교 그래프
    st.subheader("📊 알고리즘별 품종 예측 확률")

    fig_probability = px.bar(
        probability_df,
        x="품종",
        y="예측 확률",
        color="알고리즘",
        barmode="group",
        text_auto=".1f",
        title="세 알고리즘의 품종별 예측 확률 비교",
        color_discrete_sequence=[
            "#3498DB",
            "#2ECC71",
            "#E67E22"
        ]
    )

    fig_probability.update_layout(
        yaxis_title="예측 확률 (%)",
        xaxis_title="붓꽃 품종",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig_probability,
        use_container_width=True
    )

    # 테스트 정확도 비교
    st.subheader("🎯 알고리즘별 테스트 정확도")

    accuracy_df = pd.DataFrame({
        "알고리즘": list(accuracies.keys()),
        "정확도": [
            value * 100
            for value in accuracies.values()
        ]
    })

    fig_accuracy = px.bar(
        accuracy_df,
        x="알고리즘",
        y="정확도",
        color="알고리즘",
        text_auto=".1f",
        title="테스트 데이터 예측 정확도 비교",
        color_discrete_sequence=[
            "#3498DB",
            "#2ECC71",
            "#E67E22"
        ]
    )

    fig_accuracy.update_layout(
        yaxis_title="정확도 (%)",
        xaxis_title="분류 알고리즘",
        yaxis_range=[0, 105],
        showlegend=False
    )

    st.plotly_chart(
        fig_accuracy,
        use_container_width=True
    )

    # 가장 높은 정확도 표시
    best_name = max(accuracies, key=accuracies.get)
    best_accuracy = accuracies[best_name] * 100

    st.info(
        f"테스트 데이터에서 가장 높은 정확도를 보인 "
        f"알고리즘은 {best_name}이며, "
        f"정확도는 {best_accuracy:.1f}%입니다."
    )

# ---------------------------------------
# 11. 꽃잎 크기 산점도
# ---------------------------------------
st.divider()

st.subheader("📈 꽃잎 길이와 꽃잎 너비 산점도")

st.write(
    "가로축은 꽃잎 길이, 세로축은 꽃잎 너비입니다. "
    "노란색 별은 사용자가 입력한 위치입니다."
)

fig = px.scatter(
    df,
    x="꽃잎 길이",
    y="꽃잎 너비",
    color="품종",
    title="붓꽃 품종별 꽃잎 크기 분포",
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
        mode="markers+text",
        name="사용자 입력 위치",
        marker=dict(
            symbol="star",
            size=25,
            color="yellow",
            line=dict(color="black", width=2)
        ),
        text=["내가 입력한 위치"],
        textposition="top center"
    )
)

fig.update_layout(
    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------
# 12. 원본 데이터 확인
# ---------------------------------------
with st.expander("📋 원본 Iris 데이터 확인하기"):

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

st.caption(
    "사용 데이터: Iris.csv | "
    "사용 특성: 꽃잎 길이, 꽃잎 너비 | "
    "분류 알고리즘: Random Forest, KNN, Logistic Regression"
)
