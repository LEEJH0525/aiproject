
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
    page_title="서울시 인구 데이터 분석",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "population.csv"


# ==========================================
# 2. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")

    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    except Exception:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    df.columns = df.columns.astype(str).str.strip()

    if "행정구역" not in df.columns:
        raise ValueError(
            "CSV 파일에 '행정구역' 열이 없습니다."
        )

    df["행정구역"] = (
        df["행정구역"]
        .astype(str)
        .str.strip()
    )

    # 자치구 이름 추출
    df["자치구"] = df["행정구역"].apply(
        lambda x: (
            re.search(r"([가-힣]+구)", x).group(1)
            if re.search(r"([가-힣]+구)", x)
            else None
        )
    )

    # 서울시 25개 자치구만 남기기
    df = df[df["자치구"].notna()].copy()

    # 숫자 데이터 변환
    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
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


def get_gender_type(col):

    # 남자 열인지 확인
    if re.search(r"(^|[_\s])남([_\s]|$)", col):
        return "남자"

    # 여자 열인지 확인
    if re.search(r"(^|[_\s])여([_\s]|$)", col):
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

        col_gender = get_gender_type(col)

        if col_gender == gender:
            candidates.append(col)

    if not candidates:
        return None

    return candidates[0]


def get_population(year, age, gender):

    col = find_column(year, age, gender)

    if col is None:
        return None

    values = pd.to_numeric(
        df[col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

    return values.fillna(0)


# ==========================================
# 4. 사이드바 메뉴
# ==========================================

st.sidebar.title("📊 서울시 인구 분석")

menu = st.sidebar.radio(
    "분석 메뉴 선택",
    [
        "🏠 메인 화면",
        "📈 자치구별 인구 분석",
        "🏆 연령별 자치구 순위"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **서울시 인구 분석 프로젝트**

    - 자치구별 남녀 인구 비교
    - 연령별 인구 분포
    - 자치구 인구 순위
    - CSV 데이터 다운로드
    """
)


# ==========================================
# 5. 메인 화면
# ==========================================

if menu == "🏠 메인 화면":

    st.title("📊 서울시 인구 데이터 분석")

    st.markdown("---")

    st.subheader("서울시 자치구 인구 분석 프로젝트")

    st.write(
        """
        서울시 인구 데이터를 활용하여
        자치구별 인구 현황과 연령별 인구 분포를
        시각적으로 분석하는 프로그램입니다.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            ### 📈 자치구별 인구 분석

            - 연도 선택
            - 자치구 선택
            - 남자 인구 그래프
            - 여자 인구 그래프
            - 연령별 남녀 인구 비교
            - 데이터 다운로드
            """
        )

    with col2:

        st.info(
            """
            ### 🏆 연령별 자치구 순위

            - 연도 선택
            - 10세 단위 연령대 선택
            - 전체 / 남자 / 여자 선택
            - 25개 자치구 순위
            - 분홍색과 파란색 그라데이션
            - 순위 데이터 다운로드
            """
        )

    st.markdown("---")

    st.success(
        "왼쪽 메뉴에서 원하는 인구 분석 기능을 선택하세요."
    )

    st.metric(
        "분석 대상 자치구",
        f"{df['자치구'].nunique()}개"
    )


# ==========================================
# 6. 자치구별 인구 분석
# ==========================================

elif menu == "📈 자치구별 인구 분석":

    st.title("📈 서울시 자치구별 인구 분석")

    st.markdown("---")

    years = get_years()

    if not years:
        st.error("연도 데이터를 찾을 수 없습니다.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "📅 연도 선택",
            years,
            index=len(years) - 1
        )

    with col2:

        districts = sorted(
            df["자치구"].dropna().unique()
        )

        selected_district = st.selectbox(
            "🏙️ 자치구 선택",
            districts
        )

    # 연령대 가져오기
    ages = get_age_groups(selected_year)

    if not ages:
        st.error("연령대 데이터를 찾을 수 없습니다.")
        st.stop()

    # 선택한 자치구 데이터
    district_data = df[
        df["자치구"] == selected_district
    ]

    if district_data.empty:
        st.warning("선택한 자치구의 데이터가 없습니다.")
        st.stop()

    district_data = district_data.iloc[0]

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

        male_value = pd.to_numeric(
            district_data[male_col],
            errors="coerce"
        )

        female_value = pd.to_numeric(
            district_data[female_col],
            errors="coerce"
        )

        male_values.append(
            0 if pd.isna(male_value) else male_value
        )

        female_values.append(
            0 if pd.isna(female_value) else female_value
        )

        valid_ages.append(age)

    if not valid_ages:
        st.error(
            "남자와 여자 연령별 데이터를 찾을 수 없습니다. "
            "CSV 열 이름을 확인해주세요."
        )
        st.stop()

    chart_df = pd.DataFrame({
        "연령대": valid_ages,
        "남자": male_values,
        "여자": female_values
    })

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

    st.markdown("---")

    st.subheader(
        f"📊 {selected_year}년 {selected_district} 연령별 인구"
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
        title=f"{selected_district} 남녀 연령별 인구 비교",
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

    # 데이터 표
    st.markdown("---")

    st.subheader("📋 연령별 인구 데이터")

    st.dataframe(
        chart_df,
        use_container_width=True,
        hide_index=True
    )

    # CSV 다운로드
    csv = chart_df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "📥 인구 데이터 CSV 다운로드",
        data=csv,
        file_name=(
            f"{selected_year}_{selected_district}_인구분석.csv"
        ),
        mime="text/csv"
    )


# ==========================================
# 7. 연령별 자치구 순위
# ==========================================

elif menu == "🏆 연령별 자치구 순위":

    st.title("🏆 서울시 연령별 자치구 인구 순위")

    st.markdown("---")

    years = get_years()

    if not years:
        st.error("연도 데이터를 찾을 수 없습니다.")
        st.stop()

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_year = st.selectbox(
            "📅 연도 선택",
            years,
            index=len(years) - 1,
            key="rank_year"
        )

    ages = get_age_groups(selected_year)

    if not ages:
        st.error("연령대 데이터를 찾을 수 없습니다.")
        st.stop()

    with col2:

        selected_age = st.selectbox(
            "👶 연령대 선택",
            ages,
            key="rank_age"
        )

    with col3:

        selected_gender = st.selectbox(
            "👤 성별 선택",
            ["전체", "남자", "여자"],
            key="rank_gender"
        )

    # 선택한 조건의 인구 데이터
    population_values = get_population(
        selected_year,
        selected_age,
        selected_gender
    )

    if population_values is None:

        st.error(
            "선택한 조건에 맞는 데이터 열이 없습니다. "
            "CSV 파일의 열 이름을 확인해주세요."
        )
        st.stop()

    # 순위 데이터 만들기
    result_df = pd.DataFrame({
        "자치구": df["자치구"].values,
        "인구수": population_values.values
    })

    result_df = (
        result_df
        .groupby("자치구", as_index=False)["인구수"]
        .sum()
        .sort_values(
            "인구수",
            ascending=False
        )
        .reset_index(drop=True)
    )

    result_df["순위"] = result_df.index + 1

    st.markdown("---")

    st.subheader(
        f"📊 {selected_year}년 {selected_age} "
        f"{selected_gender} 인구 순위"
    )

    # 1위 자치구 정보
    if not result_df.empty:

        top = result_df.iloc[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🥇 인구가 가장 많은 자치구",
                top["자치구"]
            )

        with col2:

            st.metric(
                "인구수",
                f"{top['인구수']:,.0f}명"
            )

    # 막대그래프
    graph_df = result_df.sort_values(
        "인구수",
        ascending=True
    )

    fig = px.bar(
        graph_df,
        x="인구수",
        y="자치구",
        orientation="h",
        color="순위",
        color_continuous_scale=[
            "#2563EB",
            "#60A5FA",
            "#F9A8D4",
            "#EC4899"
        ],
        text="인구수",
        labels={
            "인구수": "인구수 (명)",
            "자치구": "자치구",
            "순위": "순위"
        }
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}명",
        textposition="outside"
    )

    fig.update_layout(
        title="자치구별 인구 내림차순 순위",
        xaxis_title="인구수 (명)",
        yaxis_title="자치구",
        template="plotly_white",
        height=850,
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        tickformat=","
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # 순위표
    st.markdown("---")

    st.subheader("📋 자치구별 인구 순위표")

    display_df = result_df[
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

    # CSV 다운로드
    csv = result_df[
        ["순위", "자치구", "인구수"]
    ].to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "📥 자치구 순위 CSV 다운로드",
        data=csv,
        file_name=(
            f"{selected_year}_{selected_age}_"
            f"{selected_gender}_자치구순위.csv"
        ),
        mime="text/csv"
    )
