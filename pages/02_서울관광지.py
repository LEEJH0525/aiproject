
import streamlit as st
import folium
from streamlit_folium import st_folium
from urllib.parse import quote

st.set_page_config(
    page_title="서울 관광지 & 맛집 여행",
    page_icon="🗺️",
    layout="wide"
)

# =========================
# 서울 관광지 TOP 10
# =========================

places = [
    {"name":"명동","lat":37.5636,"lon":126.9850,
     "desc":"쇼핑, 화장품, 길거리 음식으로 유명한 관광지"},
    {"name":"남산서울타워","lat":37.5512,"lon":126.9882,
     "desc":"서울의 아름다운 전망과 야경을 감상할 수 있는 랜드마크"},
    {"name":"경복궁","lat":37.5796,"lon":126.9770,
     "desc":"조선 왕조의 궁궐과 한국의 전통문화"},
    {"name":"홍대거리","lat":37.5563,"lon":126.9236,
     "desc":"거리 공연, 카페, 젊은 문화의 중심지"},
    {"name":"코엑스 별마당도서관","lat":37.5125,"lon":127.0590,
     "desc":"아름다운 대형 서가가 있는 복합문화공간"},
    {"name":"광장시장","lat":37.5701,"lon":126.9997,
     "desc":"빈대떡과 김밥 등 한국 전통시장 음식"},
    {"name":"동대문 DDP","lat":37.5671,"lon":127.0095,
     "desc":"독특한 건축물과 전시 공간"},
    {"name":"북촌한옥마을","lat":37.5826,"lon":126.9830,
     "desc":"한국의 전통 한옥과 아름다운 골목길"},
    {"name":"롯데월드타워","lat":37.5125,"lon":127.1029,
     "desc":"서울의 전망을 즐길 수 있는 초고층 건물"},
    {"name":"인사동","lat":37.5742,"lon":126.9850,
     "desc":"전통 공예품과 한국적인 기념품 거리"}
]

# =========================
# 1박 2일 식당 일정
# =========================

food_plan = [
    {
        "day": "DAY 1",
        "day_title": "첫째 날 - 명동 맛집 여행",
        "time": "12:00",
        "meal": "점심",
        "name": "명동교자",
        "menu": "칼국수, 만두",
        "desc": "진한 국물의 칼국수와 한국식 만두를 맛볼 수 있는 유명한 식당입니다.",
        "lat": 37.5609,
        "lon": 126.9850
    },
    {
        "day": "DAY 1",
        "day_title": "첫째 날 - 명동 맛집 여행",
        "time": "18:00",
        "meal": "저녁",
        "name": "왕비집 명동본점",
        "menu": "한국식 갈비, 고기구이",
        "desc": "한국식 숯불구이와 다양한 반찬을 함께 즐길 수 있습니다.",
        "lat": 37.5622,
        "lon": 126.9855
    },
    {
        "day": "DAY 2",
        "day_title": "둘째 날 - 전통시장과 인사동 맛집 여행",
        "time": "08:30",
        "meal": "아침",
        "name": "명동 대가",
        "menu": "한식, 국물 요리",
        "desc": "다양한 한식 메뉴를 즐길 수 있는 명동 지역 식당입니다.",
        "lat": 37.5622,
        "lon": 126.9858
    },
    {
        "day": "DAY 2",
        "day_title": "둘째 날 - 전통시장과 인사동 맛집 여행",
        "time": "12:00",
        "meal": "점심",
        "name": "개성만두궁",
        "menu": "개성식 만두, 만둣국",
        "desc": "전통적인 개성식 만두 요리를 맛볼 수 있는 인사동 식당입니다.",
        "lat": 37.5746,
        "lon": 126.9854
    },
    {
        "day": "DAY 2",
        "day_title": "둘째 날 - 전통시장과 인사동 맛집 여행",
        "time": "15:00",
        "meal": "간식",
        "name": "광장시장",
        "menu": "빈대떡, 마약김밥, 호떡",
        "desc": "다양한 한국 길거리 음식과 전통시장의 분위기를 경험해 보세요.",
        "lat": 37.5701,
        "lon": 126.9997
    }
]

# =========================
# 제목 및 언어 선택
# =========================

st.title("🗺️ 서울 관광 & 맛집 여행 TOP 10")

st.write(
    "서울의 인기 관광지와 1박 2일 한국 음식 여행을 소개합니다."
)

language = st.radio(
    "언어 선택 / Language",
    ["한국어", "English"],
    horizontal=True
)

english = language == "English"

# =========================
# 서울 지도 만들기
# =========================

st.subheader("📍 서울 주요 관광지 지도")

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커
for i, p in enumerate(places):

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=p["name"],
        popup=f"""
        <b>{p['name']}</b><br>
        {p['desc']}
        """,
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#2563eb;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                text-align:center;
                line-height:27px;
                font-weight:bold;">
                {i+1}
            </div>
            """
        )
    ).add_to(m)

# 식당 마커
for f in food_plan:

    folium.Marker(
        location=[f["lat"], f["lon"]],
        tooltip=f"{f['day']} {f['meal']} - {f['name']}",
        popup=f"""
        <b>{f['name']}</b><br>
        {f['meal']} / {f['time']}<br>
        추천 메뉴: {f['menu']}<br>
        {f['desc']}
        """,
        icon=folium.Icon(
            color="red",
            icon="cutlery",
            prefix="fa"
        )
    ).add_to(m)

# 지도 출력
st_folium(
    m,
    width=None,
    height=550,
    use_container_width=True
)

st.caption("🔵 파란색 번호: 관광지 / 🔴 빨간색: 식당 일정")

# =========================
# 1박 2일 식당 여행 일정
# =========================

st.divider()

st.title("🍽️ 서울 1박 2일 맛집 여행")

st.write(
    "서울에서 꼭 경험해 볼 만한 한국 음식과 식당을 "
    "첫째 날과 둘째 날로 나누어 소개합니다."
)

# 첫째 날
st.header("🌞 DAY 1 - 첫째 날")

st.info("명동을 중심으로 한국 음식을 즐기는 코스입니다.")

for f in food_plan:

    if f["day"] == "DAY 1":

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"### {f['time']}")
                st.caption(f["meal"])

            with col2:
                st.subheader(f["name"])
                st.write(f"🍴 추천 메뉴: {f['menu']}")
                st.write(f["desc"])

                url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    + quote(f["name"] + " 서울")
                )

                st.link_button(
                    "📍 식당 위치 확인",
                    url
                )

# 둘째 날
st.header("🌸 DAY 2 - 둘째 날")

st.info("명동에서 인사동과 광장시장으로 이동하는 코스입니다.")

for f in food_plan:

    if f["day"] == "DAY 2":

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"### {f['time']}")
                st.caption(f["meal"])

            with col2:
                st.subheader(f["name"])
                st.write(f"🍴 추천 메뉴: {f['menu']}")
                st.write(f["desc"])

                url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    + quote(f["name"] + " 서울")
                )

                st.link_button(
                    "📍 식당 위치 확인",
                    url
                )

# =========================
# 관광지 설명
# =========================

st.divider()

st.title("🏛️ 서울 관광지 TOP 10 소개")

for i in range(0, len(places), 2):

    col1, col2 = st.columns(2)

    for col, p in zip(
        [col1, col2],
        places[i:i+2]
    ):

        with col:

            with st.container(border=True):

                st.subheader(
                    f"{places.index(p)+1}. {p['name']}"
                )

                st.write(p["desc"])

                url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    f"{p['lat']},{p['lon']}"
                )

                st.link_button(
                    "Google 지도에서 보기",
                    url
                )

# =========================
# 하단 안내
# =========================

st.divider()

st.caption(
    "서울 관광 및 맛집 여행 추천 서비스"
)

st.caption(
    "지도 데이터 © OpenStreetMap contributors"
)

st.caption(
    "식당 운영시간과 메뉴는 방문 전에 확인하세요. "
    "지도상의 식당 위치는 참고용입니다."
)
