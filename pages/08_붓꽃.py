
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎 길이와 너비를 입력하여 붓꽃 품종을 예측해 보세요.")

# --------------------------------
# 1. CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():

    current_folder = Path(__file__).resolve().parent

    # 같은 폴더 또는 상위 폴더에서 CSV 찾기
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
            "Iris.csv 파일을 찾을 수 없습니다. "
            "프로젝트 폴더 또는 상위 폴더에 넣어주세요."
        )

    # 기존 CSV 파일 그대로 사용
    data = pd.read_csv(file_path, encoding="cp949")

    # 컬럼명 앞뒤 공백 제거
    data.columns = data.columns.str.strip()

    # 필요한 컬럼 확인
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
# 2. 데이터 준비
# --------------------------------
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

# 입력 범위
length_min = float(df["꽃잎 길이"].min())
length_max = float(df["꽃잎 길이"].max())

width_min = float(df["꽃잎 너비"].min())
width_max = float(df["꽃잎 너비"].max())

# --------------------------------
# 3. 학습 및 테스트 데이터
# --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------
# 4. 랜덤 포레스트 모델
# --------------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = accuracy_score(
    y_test,
    model.predict(X_test)
)

# 전체 데이터로 최종 학습
model.fit(X, y)

# --------------------------------
# 5. 데이터 정보
# --------------------------------
st.subheader("📊 데이터 분석")

c1, c2, c3 = st.columns(3)

c1.metric("전체 데이터", f"{len(df)}개")
c2.metric("품종 종류", f"{y.nunique()}종")
c3.metric("모델 정확도", f"{accuracy * 100:.1f}%")

st.divider()

# --------------------------------
# 6. 사용자 입력
# --------------------------------
st.subheader("✏️ 꽃잎 크기 입력")

st.info(
    f"""
    **입력 가능한 범위**

    - 꽃잎 길이: {length_min} ~ {length_max} cm
    - 꽃잎 너비: {width_min} ~ {width_max} cm
    """
)

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
# 7. 예측
# --------------------------------
if st.button("🌸 붓꽃 품종 예측하기", type="primary"):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    st.success(f"예측 결과: {prediction}")

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
        title="붓꽃 품종별 예측 확률"
    )

    fig_prob.update_layout(
        yaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_prob, use_container_width=True)

# --------------------------------
# 8. 산점도 그래프
# --------------------------------
st.divider()

st.subheader("📈 꽃잎 길이와 꽃잎 너비 그래프")

fig = px.scatter(
    df,
    x="꽃잎 길이",
    y="꽃잎 너비",
    color="품종",
    color_discrete_map={
        "setosa": "#3498DB",
        "versicolor": "#2ECC71",
        "virginica": "#E74C3C"
    },
    title="붓꽃 품종별 꽃잎 크기"
)

# 사용자 입력 위치
fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],
        mode="markers",
        name="내가 입력한 위치",
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
# 9. 원본 데이터 확인
# --------------------------------
with st.expander("원본 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)

st.caption("분류 알고리즘: Random Forest")
