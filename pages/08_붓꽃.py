
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --------------------------------
# 1. 페이지 기본 설정
# --------------------------------
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃(Iris) 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하면 붓꽃의 품종을 예측합니다.")

st.divider()

# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Iris.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "Iris.csv 파일을 app.py와 같은 폴더에 넣어주세요."
        )

    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    data.columns = data.columns.str.strip()

    required_columns = [
        "꽃잎 길이",
        "꽃잎 너비",
        "품종"
    ]

    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"CSV 파일에 '{col}' 컬럼이 없습니다.")

    data = data.dropna(subset=required_columns).copy()

    data["품종"] = (
        data["품종"].astype(str).str.strip()
        .str.replace("Iris-", "", regex=False)
    )

    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

# --------------------------------
# 3. 사용할 데이터와 범위 설정
# --------------------------------
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

petal_length_min = float(df["꽃잎 길이"].min())
petal_length_max = float(df["꽃잎 길이"].max())

petal_width_min = float(df["꽃잎 너비"].min())
petal_width_max = float(df["꽃잎 너비"].max())

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
# 5. 랜덤 포레스트 분류 모델
# --------------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 테스트 데이터로 성능 평가
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# 전체 데이터로 최종 모델 학습
model.fit(X, y)

# --------------------------------
# 6. 데이터 정보 표시
# --------------------------------
st.subheader("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

col1.metric("전체 데이터 개수", f"{len(df)}개")
col2.metric("붓꽃 품종 개수", f"{y.nunique()}종")
col3.metric("모델 예측 정확도", f"{accuracy * 100:.1f}%")

st.divider()

# --------------------------------
# 7. 사용자 입력
# --------------------------------
st.subheader("✏️ 꽃잎 크기 입력하기")

st.info(
    f"""
    입력 가능한 값의 범위

    🌸 꽃잎 길이: {petal_length_min} ~ {petal_length_max} cm

    🌸 꽃잎 너비: {petal_width_min} ~ {petal_width_max} cm

    ※ 입력 범위는 업로드한 Iris.csv의 실제 데이터 최솟값과 최댓값입니다.
    """
)

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=petal_length_min,
        max_value=petal_length_max,
        value=3.8,
        step=0.1,
        format="%.1f"
    )

with col2:
    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=petal_width_min,
        max_value=petal_width_max,
        value=1.2,
        step=0.1,
        format="%.1f"
    )

# --------------------------------
# 8. 품종 예측
# --------------------------------
if st.button("🌸 붓꽃 품종 예측하기", type="primary",
             use_container_width=True):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.success(f"예측된 붓꽃 품종은 {prediction} 입니다!")

    st.subheader("🔍 품종 예측 결과")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric("예측 품종", prediction)

    with result_col2:
        st.metric(
            "예측 확률",
            f"{probabilities[list(model.classes_).index(prediction)] * 100:.1f}%"
        )

    # 품종별 예측 확률
    probability_df = pd.DataFrame({
        "품종": model.classes_,
        "예측 확률": probabilities * 100
    })

    fig_prob = px.bar(
        probability_df,
        x="품종",
        y="예측 확률",
        color="품종",
        text_auto=".1f",
        title="품종별 예측 확률 (%)"
    )

    fig_prob.update_layout(
        yaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_prob, use_container_width=True)

# --------------------------------
# 9. 꽃잎 길이와 너비 산점도
# --------------------------------
st.divider()
st.subheader("📈 꽃잎 길이와 꽃잎 너비 비교")

st.write(
    "가로축은 꽃잎 길이, 세로축은 꽃잎 너비입니다. "
    "노란색 별은 사용자가 입력한 위치를 나타냅니다."
)

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
    hover_data=["품종"],
    title="붓꽃 품종별 꽃잎 크기 분포"
)

# 사용자가 입력한 위치 표시
fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],
        mode="markers+text",
        name="사용자 입력 위치",
        marker=dict(
            symbol="star",
            size=24,
            color="yellow",
            line=dict(color="black", width=2)
        ),
        text=["입력 위치"],
        textposition="top center"
    )
)

fig.update_layout(
    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",
    legend_title="붓꽃 품종",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# 10. 데이터 미리보기
# --------------------------------
with st.expander("📋 원본 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)

st.caption(
    "분류 알고리즘: Random Forest | "
    "학습 데이터: Iris.csv"
)

