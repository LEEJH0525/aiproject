
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from pathlib import Path


# ==========================================
# 1. 기본 설정
# ==========================================

st.set_page_config(
    page_title="서울시 인구 분석",
    page_icon="📊",
    layout="wide"
)

# CSV 파일은 상위 폴더에 있음
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "population.csv"


# ==========================================
# 2. CSV 데이터 불러오기
# ==========================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")

    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    df.columns = df.columns.astype(str).str.strip()

    if "행정구역" not in df.columns:
        raise ValueError("'행정구역' 열을 찾을 수 없습니다.")

    df["행정구역"] = df["행정구역"].astype(str).str.strip()

    # 서울시 자치구 이름 추출
    # 동 단위 데이터가 아닌 자치구 합계 행만 선택
    df["자치구"] = df["행정구역"].apply(
        lambda x: (
            re.search(r"([가-힣]+구)$", x).group(1)
            if re.search(r"([가-힣]+구)$", x)
            else None
        )
    )

    # 서울시 25개 자치구만 사용
    df = df[df["자치구"].notna()].copy()

    # 자치구별 데이터가 여러 행이면 합계 처리
    df = (
        df.groupby("자치구", as_index=False)
        .first()
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러올 수 없습니다: {e}")
    st.stop()


# ==========================================
# 3. 공통 함수
# ==========================================

def get_years():

    years = set()

    for col in df.columns:

        match = re.search(r"(20\d{2})년", col)

        if match:
            years.add(match.group(1))

    return sorted(years)


def get_age_groups(year):

    ages = set()

    for col in df.columns:

        if f"{year}년" not in col:
            continue

        match = re.search(
            r"(\d+\s*~\s*\d+세|\d+세\s*이상)",
            col
        )

        if match:
            age = re.sub(r"\s+", "", match.group(1))
            ages.add(age)

    def age_sort(age):
        match = re.search(r"\d+", age)
        return int(match.group()) if match else 999

    return sorted(ages, key=age_sort)


def get_gender(col):

    if re.search(r"남", col):
        return "남자"

    if re.search(r"여", col):
        return "여자"

    return "전체"


def find_column(year, age, gender):

    age_pattern = age.replace("~", r"\s*~\s*")

    candidates = []

    for col in df.columns:

        if f"{year}년" not in col:
            continue

        if not re.search(age_pattern, col):
            continue

        col_gender = get_gender(col)

        if col_gender == gender:
            candidates.append(col)

    if not candidates:
        return None

    return candidates[0]


def get_number(value):

    return pd.to_numeric(
        str(value).replace(",", ""),
        errors="coerce"
    )


def get_district_age_population(year, age):

    """
    선택한 연령대의 자치구별 전체 인구를 가져옴.
    전체 인구 열이 없으면 남자와 여자 인구를 더함.
    """

    total_col = find_column(year, age, "전체")
    male_col = find_column(year, age, "남자")
    female_col = find_column(year, age, "여자")

    if total_col is not None:

        values = pd.to_numeric(
            df[total_col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        ).fillna(0)

    elif male_col is not None and female_col is not None:

        male = pd.to_numeric(
            df[male_col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        ).fillna(0)

        female = pd.to_numeric(
            df[female_col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        ).fillna(0)

        values = male + female

    else:
        return None

    return values


# ==========================================
# 4. 페이지 제목
# ==========================================

st.title("📊 서울시 자치구별 인구 분석")

st.markdown(
    """
    서울시 자치구별 남녀 인구와 연령대별 인구 순위를
    한눈에 비교할 수 있습니다.
    """
)

st.markdown("---")


# ==========================================
# 5. 연도 및 자치구 선택
# ==========================================

years = get_years()

if not years:
    st.error("CSV 파일에서 연도 데이터를 찾을 수 없습니다.")
    st.stop()

col1, col2 = st.columns(2)

with col1:

    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1
    )

with col2:

    districts = sorted(df["자치구"].unique())

    selected_district = st.selectbox(
        "🏙️ 자치구 선택",
        districts
    )


# ==========================================
# 6. 기존 남녀 연령별 인구 분석
# ==========================================

st.markdown("---")

st.header("1️⃣ 자치구별 남녀 연령 인구 분석")

district_data = df[
    df["자치구"] == selected_district
]

if district_data.empty:
    st.error("선택한 자치구의 데이터가 없습니다.")
    st.stop()

district_data = district_data.iloc[0]

ages = get_age_groups(selected_year)

male_values = []
female_values = []
valid_ages = []

for age in ages:

    male_col = find_column(
        selected_year,
        age,
        "남자"
    )

    female_col = find_column(
        selected_year,
        age,
        "여자"
    )

    if male_col is None or female_col is None:
        continue

    male_value = get_number(district_data[male_col])
    female_value = get_number(district_data[female_col])

    male_values.append(
        0 if pd.isna(male_value) else male_value
    )

    female_values.append(
        0 if pd.isna(female_value) else female_value
    )

    valid_ages.append(age)


if not valid_ages:
    st.error(
        "남자와 여자 연령별 데이터를 찾지 못했습니다. "
        "CSV 파일의 열 이름을 확인해주세요."
    )
    st.stop()


chart_df = pd.DataFrame({
    "연령대": valid_ages,
    "남자": male_values,
    "여자": female_values
})


# 남녀 인구 합계
total_male = sum(male_values)
total_female = sum(female_values)
total_population = total_male + total_female


# 인구 요약
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "선택한 자치구",
        selected_district
    )

with col2:
    st.metric(
        "남자 인구",
        f"{total_male:,.0f}명"
    )

with col3:
    st.metric(
        "여자 인구",
        f"{total_female:,.0f}명"
    )


# 남녀 선 그래프
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["연령대"],
        y=chart_df["남자"],
        mode="lines+markers",
        name="남자",
        line=dict(
            color="#FF69B4",
            width=3
        ),
        marker=dict(size=7)
    )
)

fig.add_trace(
    go.Scatter(
        x=chart_df["연령대"],
        y=chart_df["여자"],
        mode="lines+markers",
        name="여자",
        line=dict(
            color="#16A34A",
            width=3
        ),
        marker=dict(size=7)
    )
)

fig.update_layout(
    title=f"{selected_year}년 {selected_district} 남녀 연령별 인구",
    xaxis_title="연령대",
    yaxis_title="인구수 (명)",
    hovermode="x unified",
    template="plotly_white",
    height=550
)

fig.update_yaxes(
    tickformat=",",
    dtick=1000
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 기존 인구 데이터 표
st.subheader("📋 남녀 연령별 인구 데이터")

st.dataframe(
    chart_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 7. 추가 기능: 연령대별 자치구 순위
# ==========================================

st.markdown("---")

st.header("2️⃣ 연령대별 서울시 자치구 인구 순위")

st.write(
    "원하는 연령대를 선택하면 서울시 25개 자치구의 "
    "인구가 많은 순서대로 막대그래프가 표시됩니다."
)


# 연령대 선택
rank_ages = get_age_groups(selected_year)

selected_rank_age = st.selectbox(
    "👶 비교할 연령대 선택",
    rank_ages,
    key="rank_age"
)


# 선택한 연령대의 25개 자치구 인구
rank_values = get_district_age_population(
    selected_year,
    selected_rank_age
)

if rank_values is None:

    st.error(
        "선택한 연령대의 전체 인구 데이터를 찾을 수 없습니다. "
        "남자와 여자 인구 열도 확인해주세요."
    )
    st.stop()


# 순위 데이터 생성
rank_df = pd.DataFrame({
    "자치구": df["자치구"].values,
    "인구수": rank_values.values
})


# 인구가 많은 순서대로 정렬
rank_df = (
    rank_df
    .dropna(subset=["인구수"])
    .sort_values(
        "인구수",
        ascending=False
    )
    .reset_index(drop=True)
)

rank_df["순위"] = rank_df.index + 1


# 1위 정보 표시
if not rank_df.empty:

    top_district = rank_df.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🥇 인구가 가장 많은 자치구",
            top_district["자치구"]
        )

    with col2:

        st.metric(
            "인구수",
            f"{top_district['인구수']:,.0f}명"
        )


# ==========================================
# 8. 자치구 순위 막대그래프
# ==========================================

st.subheader(
    f"📊 {selected_rank_age} 인구 자치구 순위"
)

# 그래프는 낮은 순위부터 그려서
# 높은 순위가 위쪽에 보이도록 설정
graph_df = rank_df.sort_values(
    "인구수",
    ascending=True
).copy()

fig2 = px.bar(
    graph_df,
    x="인구수",
    y="자치구",
    orientation="h",
    color="순위",
    color_continuous_scale=[
        "#EC4899",
        "#F9A8D4",
        "#93C5FD",
        "#2563EB"
    ],
    text="인구수",
    labels={
        "인구수": "인구수 (명)",
        "자치구": "자치구",
        "순위": "순위"
    }
)

fig2.update_traces(
    texttemplate="%{text:,.0f}명",
    textposition="outside"
)

fig2.update_layout(
    title=f"{selected_year}년 {selected_rank_age} 자치구별 인구 순위",
    xaxis_title="인구수 (명)",
    yaxis_title="자치구",
    template="plotly_white",
    height=850,
    coloraxis_showscale=False
)

fig2.update_xaxes(
    tickformat=","
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================================
# 9. 자치구 순위표
# ==========================================

st.subheader("📋 자치구별 인구 순위표")

display_df = rank_df[
    ["순위", "자치구", "인구수"]
].copy()

display_df["인구수"] = display_df["인구수"].map(
    lambda x: f"{x:,.0f}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 10. CSV 다운로드
# ==========================================

csv = rank_df[
    ["순위", "자치구", "인구수"]
].to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 연령대별 자치구 순위 다운로드",
    data=csv,
    file_name=(
        f"{selected_year}_{selected_rank_age}_"
        "서울시_자치구순위.csv"
    ),
    mime="text/csv"
)


# ==========================================
# 11. 페이지 하단
# ==========================================

st.markdown("---")

st.caption(
    "서울시 인구 데이터 분석 | 남녀 연령별 인구 및 자치구 순위"
)
