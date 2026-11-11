
import streamlit as st

st.set_page_config(
    page_title="서울시 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 인구 데이터 분석")
st.markdown("---")

st.header("서울시 자치구 인구 분석 프로젝트")

st.write("""
이 프로젝트는 서울시 인구 데이터를 활용하여
자치구별 인구 현황과 연령대별 인구 분포를 분석합니다.
""")

st.subheader("📌 분석 기능")

col1, col2 = st.columns(2)

with col1:
    st.info("### 1. 자치구별 인구 분석")
    st.write("""
    - 연도 선택
    - 서울시 25개 자치구 선택
    - 연령별 남자 인구 그래프
    - 연령별 여자 인구 그래프
    - 남자와 여자 인구 비교
    """)

with col2:
    st.info("### 2. 연령별 자치구 순위")
    st.write("""
    - 연도 선택
    - 10세 단위 연령대 선택
    - 전체 / 남자 / 여자 선택
    - 인구가 많은 자치구부터 순위 표시
    - 막대그래프 및 데이터 다운로드
    """)

st.markdown("---")
st.success("왼쪽 메뉴에서 원하는 분석 페이지를 선택하세요.")
