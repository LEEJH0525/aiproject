
import streamlit as st

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🧭",
    layout="centered"
)

# =====================================
# 2. 디자인
# =====================================

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FF;
}

.main-title {
    text-align: center;
    color: #6558C9;
    font-size: 38px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: #777777;
    font-size: 17px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# 3. 프로그램 제목
# =====================================

st.markdown(
    '<div class="main-title">🧭 MBTI 진로 탐험소</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">나에게 어울리는 미래의 직업을 찾아보자! ✨</div>',
    unsafe_allow_html=True
)

st.write("")
st.info(
    "💡 MBTI를 선택하면 너에게 어울리는 직업 2가지를 추천해 줄게!"
)

# =====================================
# 4. MBTI별 진로 데이터
# =====================================

career_data = {

    "ISTJ": {
        "name": "청렴한 현실주의자 📚",
        "jobs": [
            {
                "job": "회계사",
                "major": "회계학과, 경영학과, 세무학과",
                "personality": "꼼꼼하고 책임감이 강하며 숫자와 자료를 정확하게 다루는 성격",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "job": "공무원",
                "major": "행정학과, 법학과, 사회학과",
                "personality": "규칙을 잘 지키고 성실하며 맡은 일을 끝까지 해내는 성격",
                "salary": "약 3,000만~5,500만 원"
            }
        ]
    },

    "ISFJ": {
        "name": "따뜻한 수호자 🌷",
        "jobs": [
            {
                "job": "간호사",
                "major": "간호학과",
                "personality": "다른 사람을 배려하고 책임감이 있으며 세심한 성격",
                "salary": "약 3,500만~5,500만 원"
            },
            {
                "job": "초등학교 교사",
                "major": "초등교육과",
                "personality": "친절하고 인내심이 많으며 다른 사람을 돕는 것을 좋아하는 성격",
                "salary": "약 4,000만~7,000만 원"
            }
        ]
    },

    "INFJ": {
        "name": "통찰력 있는 조언자 🌙",
        "jobs": [
            {
                "job": "심리상담사",
                "major": "심리학과, 상담심리학과",
                "personality": "공감 능력이 뛰어나고 다른 사람의 이야기를 잘 들어주는 성격",
                "salary": "약 3,000만~5,000만 원"
            },
            {
                "job": "사회복지사",
                "major": "사회복지학과",
                "personality": "이타적이고 따뜻하며 사회에 긍정적인 영향을 주고 싶은 성격",
                "salary": "약 2,800만~4,500만 원"
            }
        ]
    },

    "INTJ": {
        "name": "전략적인 설계자 🧠",
        "jobs": [
            {
                "job": "데이터 분석가",
                "major": "통계학과, 컴퓨터공학과, 데이터사이언스학과",
                "personality": "논리적이고 분석적이며 문제를 해결하는 것을 좋아하는 성격",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "job": "건축가",
                "major": "건축학과, 건축공학과",
                "personality": "창의적이면서도 계획적이고 공간을 설계하는 것을 좋아하는 성격",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },

    "ISTP": {
        "name": "만능 재주꾼 🔧",
        "jobs": [
            {
                "job": "기계공학 엔지니어",
                "major": "기계공학과, 자동차공학과",
                "personality": "문제 해결 능력이 뛰어나고 실용적인 활동을 좋아하는 성격",
                "salary": "약 3,800만~6,500만 원"
            },
            {
                "job": "정보보안 전문가",
                "major": "정보보호학과, 컴퓨터공학과",
                "personality": "분석적이고 침착하며 문제의 원인을 찾아내는 것을 좋아하는 성격",
                "salary": "약 4,000만~7,000만 원"
            }
        ]
    },

    "ISFP": {
        "name": "호기심 많은 예술가 🎨",
        "jobs": [
            {
                "job": "시각디자이너",
                "major": "시각디자인학과, 산업디자인학과",
                "personality": "감각적이고 창의적이며 자신만의 아이디어를 표현하는 성격",
                "salary": "약 3,000만~5,000만 원"
            },
            {
                "job": "작업치료사",
                "major": "작업치료학과",
                "personality": "세심하고 배려심이 많으며 사람들의 일상 회복을 돕는 성격",
                "salary": "약 3,000만~4,500만 원"
            }
        ]
    },

    "INFP": {
        "name": "열정적인 중재자 🌱",
        "jobs": [
            {
                "job": "작가",
                "major": "문예창작학과, 국어국문학과",
                "personality": "상상력이 풍부하고 감수성이 뛰어나며 글쓰기를 좋아하는 성격",
                "salary": "약 2,800만~5,000만 원"
            },
            {
                "job": "미술치료 전문가",
                "major": "미술치료 관련 학과, 심리학과, 미술학과",
                "personality": "공감 능력이 높고 예술을 통해 사람을 돕는 데 관심이 있는 성격",
                "salary": "약 2,800만~4,500만 원"
            }
        ]
    },

    "INTP": {
        "name": "논리적인 사색가 💡",
        "jobs": [
            {
                "job": "소프트웨어 개발자",
                "major": "컴퓨터공학과, 소프트웨어학과",
                "personality": "논리적이고 호기심이 많으며 새로운 기술을 탐구하는 성격",
                "salary": "약 4,000만~8,000만 원"
            },
            {
                "job": "연구원",
                "major": "자연과학계열, 공학계열 관련 학과",
                "personality": "탐구심이 강하고 깊이 있게 생각하며 새로운 지식을 발견하는 성격",
                "salary": "약 3,500만~6,500만 원"
            }
        ]
    },

    "ESTP": {
        "name": "모험을 즐기는 사업가 🏃",
        "jobs": [
            {
                "job": "영업 전문가",
                "major": "경영학과, 마케팅학과",
                "personality": "활동적이고 사교적이며 사람들과 소통하는 것을 좋아하는 성격",
                "salary": "약 3,500만~7,000만 원"
            },
            {
                "job": "스포츠 지도자",
                "major": "체육학과, 스포츠과학과",
                "personality": "에너지가 넘치고 도전적이며 사람들과 함께 활동하는 성격",
                "salary": "약 2,800만~5,000만 원"
            }
        ]
    },

    "ESFP": {
        "name": "자유로운 연예인 🎤",
        "jobs": [
            {
                "job": "이벤트 기획자",
                "major": "광고홍보학과, 문화콘텐츠학과",
                "personality": "밝고 사교적이며 사람들에게 즐거운 경험을 만들어 주는 성격",
                "salary": "약 3,000만~5,000만 원"
            },
            {
                "job": "홍보 및 마케팅 전문가",
                "major": "광고홍보학과, 경영학과",
                "personality": "표현력이 좋고 친화력이 뛰어나며 트렌드에 관심이 많은 성격",
                "salary": "약 3,300만~6,000만 원"
            }
        ]
    },

    "ENFP": {
        "name": "재기발랄한 활동가 🌈",
        "jobs": [
            {
                "job": "콘텐츠 기획자",
                "major": "미디어학과, 광고홍보학과",
                "personality": "아이디어가 풍부하고 새로운 시도를 즐기며 소통을 좋아하는 성격",
                "salary": "약 3,200만~5,800만 원"
            },
            {
                "job": "교육 콘텐츠 개발자",
                "major": "교육학과, 교육공학과",
                "personality": "창의적이고 사람들에게 새로운 지식을 알려주는 것을 좋아하는 성격",
                "salary": "약 3,000만~5,500만 원"
            }
        ]
    },

    "ENTP": {
        "name": "뜨거운 논쟁을 즐기는 변론가 ⚡",
        "jobs": [
            {
                "job": "서비스 기획자",
                "major": "경영학과, 산업공학과, 컴퓨터공학과",
                "personality": "아이디어가 많고 새로운 문제에 도전하는 것을 즐기는 성격",
                "salary": "약 4,000만~8,000만 원"
            },
            {
                "job": "변호사",
                "major": "법학 관련 학과, 법학전문대학원",
                "personality": "논리적이고 설득력이 있으며 토론과 문제 해결을 좋아하는 성격",
                "salary": "약 7,000만~1억 5,000만 원 이상"
            }
        ]
    },

    "ESTJ": {
        "name": "엄격한 관리자 📊",
        "jobs": [
            {
                "job": "프로젝트 관리자",
                "major": "경영학과, 산업공학과",
                "personality": "체계적이고 책임감이 강하며 목표를 달성하기 위해 계획하는 성격",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "job": "재무 관리자",
                "major": "경영학과, 경제학과, 회계학과",
                "personality": "현실적이고 꼼꼼하며 조직을 효율적으로 운영하는 성격",
                "salary": "약 4,500만~8,000만 원"
            }
        ]
    },

    "ESFJ": {
        "name": "사교적인 외교관 🤝",
        "jobs": [
            {
                "job": "인사 담당자",
                "major": "경영학과, 심리학과, 행정학과",
                "personality": "친절하고 협동심이 강하며 다른 사람들과 관계를 잘 형성하는 성격",
                "salary": "약 3,500만~6,500만 원"
            },
            {
                "job": "호텔 관리자",
                "major": "호텔경영학과, 관광경영학과",
                "personality": "서비스 정신이 뛰어나고 사교적이며 사람들을 배려하는 성격",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },

    "ENFJ": {
        "name": "정의로운 사회운동가 🌟",
        "jobs": [
            {
                "job": "교사",
                "major": "교육학과 또는 담당 교과 관련 학과",
                "personality": "리더십이 있고 공감 능력이 뛰어나며 다른 사람의 성장을 돕는 성격",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "job": "교육 및 인재개발 전문가",
                "major": "교육학과, 교육공학과, 경영학과",
                "personality": "소통을 잘하고 다른 사람의 잠재력을 발견하는 것을 좋아하는 성격",
                "salary": "약 3,500만~6,500만 원"
            }
        ]
    },

    "ENTJ": {
        "name": "대담한 통솔자 👑",
        "jobs": [
            {
                "job": "경영 컨설턴트",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "리더십과 분석력이 뛰어나고 전략적으로 목표를 세우는 성격",
                "salary": "약 5,000만~9,000만 원"
            },
            {
                "job": "변호사",
                "major": "법학 관련 학과, 법학전문대학원",
                "personality": "자신감이 있고 논리적이며 책임감과 판단력이 뛰어난 성격",
                "salary": "약 7,000만~1억 5,000만 원 이상"
            }
        ]
    }
}

# =====================================
# 5. MBTI 선택
# =====================================

st.divider()

st.header("💜 나의 MBTI 선택하기")

selected_mbti = st.selectbox(
    "나의 MBTI 유형을 골라줘!",
    list(career_data.keys()),
    index=None,
    placeholder="MBTI를 선택해 주세요."
)

# =====================================
# 6. 진로 추천 결과
# =====================================

if selected_mbti is not None:

    data = career_data[selected_mbti]

    st.divider()

    st.balloons()

    st.markdown(
        "## ✨ " + selected_mbti + " ✨"
    )

    st.subheader(data["name"])

    st.success("🎉 너에게 어울리는 진로 2가지를 찾았어!")

    for number, job in enumerate(data["jobs"], 1):

        st.markdown(
            "### " + str(number) + ". 💼 " + job["job"]
        )

        with st.container(border=True):

            st.markdown("🎓 **관련 학과**")
            st.write(job["major"])

            st.markdown("💗 **이런 성격이라면 잘 어울려!**")
            st.write(job["personality"])

            st.markdown("💰 **예상 연봉**")
            st.write(job["salary"])

        st.write("")

    # 응원 메시지

    st.divider()

    st.header("💌 나에게 전하는 응원 메시지")

    st.info(
        "너의 가능성은 MBTI 4글자로 정해지지 않아! 🌈\n\n"
        "자신이 좋아하는 일과 잘하는 일을 찾아가다 보면 "
        "분명 멋진 미래를 만들어 갈 수 있을 거야. 💕"
    )

else:

    st.warning("👇 먼저 자신의 MBTI를 선택해 줘!")

# =====================================
# 7. 하단 안내
# =====================================

st.divider()

st.caption(
    "📌 연봉은 국내 직업의 참고용 추정 범위이며 "
    "실제 평균 연봉과 차이가 있을 수 있습니다."
)

st.caption(
    "📌 실제 연봉은 경력, 기업 규모, 근무 지역 및 직무에 따라 달라집니다."
)

st.markdown(
    "[🔎 한국고용정보원 직업정보 확인하기](https://www.work.go.kr)"
)

st.caption("🧭 MBTI 진로 탐험소 | 나의 꿈을 찾아가는 시간 ✨")
