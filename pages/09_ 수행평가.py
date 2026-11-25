
import streamlit as st

# --------------------------------------
# 기본 설정
# --------------------------------------
st.set_page_config(
    page_title="K-POP IDOL WORLD",
    page_icon="🎤",
    layout="wide"
)

# --------------------------------------
# 아이돌 그룹 정보
# --------------------------------------
idol_groups = {
    "보이넥스트도어": {
        "english": "BOYNEXTDOOR",
        "members": 6,
        "names": "성호, 리우, 명재현, 태산, 이한, 운학",
        "debut": "2023년 5월 30일",
        "agency": "KOZ 엔터테인먼트",
        "description": "청춘의 일상과 감정을 솔직하고 친근하게 표현하는 보이그룹입니다.",
        "awards": [
            "2023 멜론뮤직어워드 글로벌 라이징 아티스트",
            "2023 골든디스크어워즈 넥스트 제너레이션",
            "2024 멜론뮤직어워드 남자 퍼포먼스상"
        ],
        "summary": [
            "2023년 5월 30일 KOZ 엔터테인먼트에서 데뷔한 6인조 그룹입니다.",
            "멤버는 성호, 리우, 명재현, 태산, 이한, 운학입니다.",
            "청춘의 일상과 사랑을 음악으로 표현합니다.",
            "대표곡은 One and Only, Earth, Wind & Fire 등이 있습니다.",
            "골든디스크어워즈 넥스트 제너레이션 등 여러 상을 수상했습니다."
        ],
        "mv_title": "ANIMAL",
        "mv_date": "2026년 9월 28일",
        "mv_id": "WI4__7z_dJw"
    },

    "투모로우바이투게더": {
        "english": "TXT",
        "members": 5,
        "names": "수빈, 연준, 범규, 태현, 휴닝카이",
        "debut": "2019년 3월 4일",
        "agency": "빅히트 뮤직",
        "description": "청춘과 성장, 우정에 대한 이야기를 음악으로 전달하는 그룹입니다.",
        "awards": [
            "2019 멜론뮤직어워드 남자 신인상",
            "2019 MAMA 남자 신인상",
            "2021 일본 골드디스크 대상 아시아 부문 신인상",
            "2025 골든디스크어워즈 음반 본상"
        ],
        "summary": [
            "2019년 3월 4일 빅히트 뮤직에서 데뷔한 5인조 그룹입니다.",
            "멤버는 수빈, 연준, 범규, 태현, 휴닝카이입니다.",
            "청춘과 성장에 관한 이야기를 음악으로 표현합니다.",
            "대표곡은 0X1=LOVESONG, Sugar Rush Ride 등이 있습니다.",
            "다양한 국내외 시상식에서 신인상과 본상을 수상했습니다."
        ],
        "mv_title": "Angel Bite",
        "mv_date": "2026년 11월 16일",
        "mv_id": "Cf3daiQ4lBU"
    },

    "코르티스": {
        "english": "CORTIS",
        "members": 5,
        "names": "마틴, 제임스, 주훈, 성현, 건호",
        "debut": "2025년 8월 18일",
        "agency": "빅히트 뮤직",
        "description": "자유로운 창작과 개성 있는 음악을 추구하는 보이그룹입니다.",
        "awards": [
            "2025년 데뷔 앨범 COLOR OUTSIDE THE LINES 발표",
            "2025년 데뷔 활동 및 신인 아티스트 활동",
            "2026년 음악 활동 및 글로벌 팬덤 확대"
        ],
        "summary": [
            "2025년 8월 18일 빅히트 뮤직에서 데뷔한 5인조 그룹입니다.",
            "멤버는 마틴, 제임스, 주훈, 성현, 건호입니다.",
            "자유로운 창작과 독특한 음악 스타일이 특징입니다.",
            "대표곡으로는 GO!, FaSHioN, ACAI 등이 있습니다.",
            "국내외에서 빠르게 팬층을 넓혀가고 있는 그룹입니다."
        ],
        "mv_title": "PACK IT UP",
        "mv_date": "2026년 8월 24일",
        "mv_id": "TZWiMoQpr8c"
    },

    "아이브": {
        "english": "IVE",
        "members": 6,
        "names": "안유진, 가을, 레이, 장원영, 리즈, 이서",
        "debut": "2021년 12월 1일",
        "agency": "스타쉽 엔터테인먼트",
        "description": "자신감 있고 당당한 매력을 음악과 무대로 표현하는 걸그룹입니다.",
        "awards": [
            "2022 멜론뮤직어워드 올해의 신인상",
            "2022 MAMA 여자 신인상",
            "2023 골든디스크어워즈 디지털 음원 대상",
            "2024 MAMA 월드와이드 팬스 초이스"
        ],
        "summary": [
            "2021년 12월 1일 스타쉽 엔터테인먼트에서 데뷔한 6인조 걸그룹입니다.",
            "멤버는 안유진, 가을, 레이, 장원영, 리즈, 이서입니다.",
            "자신감과 자기애를 강조하는 음악이 특징입니다.",
            "대표곡은 ELEVEN, LOVE DIVE, After LIKE 등이 있습니다.",
            "신인상과 골든디스크어워즈 디지털 음원 대상 등 다양한 상을 수상했습니다."
        ],
        "mv_title": "Looks Can Kill",
        "mv_date": "2026년 10월 19일",
        "mv_id": "rsnhwkc4nee"
    },

    "에이티즈": {
        "english": "ATEEZ",
        "members": 8,
        "names": "홍중, 성화, 윤호, 여상, 산, 민기, 우영, 종호",
        "debut": "2018년 10월 24일",
        "agency": "KQ 엔터테인먼트",
        "description": "강렬한 퍼포먼스와 독창적인 세계관이 특징인 글로벌 보이그룹입니다.",
        "awards": [
            "2020 MAMA 디스커버리 오브 더 이어",
            "2020 MAMA 월드와이드 팬스 초이스",
            "2023 빌보드 200 앨범 차트 1위 기록"
        ],
        "summary": [
            "2018년 10월 24일 KQ 엔터테인먼트에서 데뷔한 8인조 그룹입니다.",
            "멤버는 홍중, 성화, 윤호, 여상, 산, 민기, 우영, 종호입니다.",
            "강렬한 퍼포먼스와 독창적인 세계관이 특징입니다.",
            "대표곡은 WONDERLAND, BOUNCY, Guerrilla 등이 있습니다.",
            "MAMA 수상과 빌보드 200 1위 등의 글로벌 성과를 거뒀습니다."
        ],
        "mv_title": "BAD (Japanese Ver.)",
        "mv_date": "2026년 11월 13일",
        "mv_id": "SGovymtCzvA"
    }
}

# --------------------------------------
# 글로벌 인기도 예시 점수
# --------------------------------------
popularity = {
    "아이브": 95,
    "투모로우바이투게더": 90,
    "에이티즈": 86,
    "보이넥스트도어": 82,
    "코르티스": 78
}

# --------------------------------------
# 제목
# --------------------------------------
st.title("🎤 K-POP IDOL WORLD 🌟")

st.subheader("내가 좋아하는 아이돌 그룹을 알아보자!")

st.write(
    "K-POP 인기 아이돌 5개 그룹의 정보와 "
    "최신 뮤직비디오, 글로벌 인기도를 알아보세요!"
)

st.divider()

# --------------------------------------
# 그룹 선택
# --------------------------------------
selected = st.selectbox(
    "💖 소개받고 싶은 아이돌 그룹을 선택하세요!",
    list(idol_groups.keys())
)

data = idol_groups[selected]

# --------------------------------------
# 기본 정보
# --------------------------------------
st.header("✨ " + selected)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 멤버 수", str(data["members"]) + "명")

with col2:
    st.metric("📅 데뷔일", data["debut"])

with col3:
    st.metric("🏢 소속사", data["agency"])

st.divider()

# --------------------------------------
# 멤버 소개
# --------------------------------------
st.subheader("👑 멤버 소개")

st.write("**그룹 이름:**", data["english"])
st.write("**멤버 이름:**", data["names"])

st.info(data["description"])

st.divider()

# --------------------------------------
# 최신 뮤직비디오
# --------------------------------------
st.header("🎬 최신 뮤직비디오")

st.subheader("🎵 " + data["mv_title"])

st.write("📅 공개일:", data["mv_date"])

st.video(
    "https://www.youtube.com/watch?v=" + data["mv_id"]
)

st.caption("※ 등록된 유튜브 영상 ID를 사용합니다.")

st.divider()

# --------------------------------------
# 수상 경력
# --------------------------------------
st.subheader("🏆 주요 수상 및 활동 기록")

for i, award in enumerate(data["awards"], 1):
    st.write(f"**{i}.** 🏆 {award}")

st.divider()

# --------------------------------------
# 5줄 요약
# --------------------------------------
st.subheader("📝 5줄 핵심 요약")

for i, sentence in enumerate(data["summary"], 1):
    st.markdown(f"**{i}.** {sentence}")

st.divider()

# --------------------------------------
# 글로벌 인기도 막대그래프
# --------------------------------------
st.header("🌍 세계 K-POP 그룹 인기도 비교")

st.write(
    "5개 아이돌 그룹의 인기도 비교용 점수를 "
    "막대그래프로 확인해 보세요!"
)

st.info(
    "📌 아래 점수는 그래프 디자인과 기능을 위한 예시 점수입니다. "
    "실제 세계 팬 수나 공식 글로벌 인기 순위는 아닙니다."
)

# 높은 점수부터 정렬
sorted_groups = sorted(
    popularity.items(),
    key=lambda x: x[1],
    reverse=True
)

# 핑크색 그라데이션
colors = [
    "#FF1493",
    "#FF4DA6",
    "#FF80BF",
    "#FFADD6",
    "#FFD1E8"
]

st.subheader("📊 그룹별 글로벌 인기도 순위")

# 그래프를 한글로 직접 구성
for rank, (group, score) in enumerate(sorted_groups):

    color = colors[rank]

    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown(f"### {rank + 1}위")

    with col2:
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:space-between;
                font-weight:bold;
                margin-bottom:5px;
                color:inherit;
            ">
                <span>{group}</span>
                <span>{score}점</span>
            </div>
            <div style="
                width:100%;
                height:30px;
                background-color:#EEEEEE;
                border-radius:10px;
                overflow:hidden;
            ">
                <div style="
                    width:{score}%;
                    height:30px;
                    background-color:{color};
                    border-radius:10px;
                ">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption(
    "🌸 1위는 진한 핑크색이며, 순위가 낮아질수록 "
    "연한 핑크색으로 표시됩니다."
)

st.divider()

# --------------------------------------
# 인기 점수 비교 표
# --------------------------------------
st.subheader("🏅 그룹별 순위표")

for rank, (group, score) in enumerate(sorted_groups, 1):
    st.write(
        f"**{rank}위 | {group} | {score}점**"
    )

st.divider()

# --------------------------------------
# 전체 그룹 비교
# --------------------------------------
st.header("🎵 아이돌 그룹 한눈에 비교")

for group_name, group_data in idol_groups.items():

    with st.expander("💗 " + group_name):

        st.write("**멤버 수:**", str(group_data["members"]) + "명")
        st.write("**멤버 이름:**", group_data["names"])
        st.write("**데뷔일:**", group_data["debut"])
        st.write("**소속사:**", group_data["agency"])
        st.write("**최신 뮤직비디오:**", group_data["mv_title"])

        st.write("**주요 수상 및 활동:**")

        for award in group_data["awards"]:
            st.write("- " + award)

st.divider()

st.success(
    "🎉 K-POP IDOL WORLD에서 좋아하는 아이돌을 만나 보세요!"
)

st.caption(
    "K-POP IDOL WORLD | 아이돌 정보 및 뮤직비디오 소개"
)
