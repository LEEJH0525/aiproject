
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 관광지 데이터
places = [
    {
        "name": "명동",
        "en": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9850,
        "desc": "쇼핑, 화장품 매장, 길거리 음식으로 유명한 서울 대표 관광지입니다.",
        "desc_en": "A famous shopping district with cosmetics, fashion and Korean street food."
    },
    {
        "name": "남산서울타워",
        "en": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울의 아름다운 전경과 야경을 감상할 수 있는 대표 랜드마크입니다.",
        "desc_en": "A famous landmark offering beautiful views of Seoul."
    },
    {
        "name": "경복궁",
        "en": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 왕조의 궁궐로 한국의 역사와 전통문화를 경험할 수 있습니다.",
        "desc_en": "The main royal palace of the Joseon Dynasty."
    },
    {
        "name": "홍대거리",
        "en": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "젊은 문화와 거리 공연, 개성 있는 카페와 상점이 유명합니다.",
        "desc_en": "A lively area famous for street performances, cafes and shopping."
    },
    {
        "name": "코엑스 별마당도서관",
        "en": "Starfield Library",
        "lat": 37.5125,
        "lon": 127.0590,
        "desc": "높은 책장과 독특한 인테리어로 유명한 아름다운 도서관입니다.",
        "desc_en": "A beautiful library with impressive bookshelves."
    },
    {
        "name": "광장시장",
        "en": "Gwangjang Market",
        "lat": 37.5701,
        "lon": 126.9997,
        "desc": "빈대떡과 김밥 등 다양한 한국 전통 음식을 맛볼 수 있습니다.",
        "desc_en": "A traditional market famous for Korean street food."
    },
    {
        "name": "동대문디자인플라자",
        "en": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "desc": "독특한 건축 디자인과 전시, 문화행사를 즐길 수 있습니다.",
        "desc_en": "A futuristic building with exhibitions and cultural events."
    },
    {
        "name": "북촌한옥마을",
        "en": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥과 아름다운 골목길을 만날 수 있는 관광지입니다.",
        "desc_en": "A beautiful traditional Korean village."
    },
    {
        "name": "롯데월드타워",
        "en": "Lotte World Tower",
        "lat": 37.5125,
        "lon": 127.1029,
        "desc": "서울의 스카이라인을 감상할 수 있는 초고층 랜드마크입니다.",
        "desc_en": "A famous skyscraper with an observation deck."
    },
    {
        "name": "인사동",
        "en": "Insadong",
        "lat": 37.5742,
        "lon": 126.9850,
        "desc": "전통 공예품, 갤러리, 찻집과 한국적인 기념품으로 유명합니다.",
        "desc_en": "A cultural street with traditional crafts, galleries and tea houses."
    }
]

# 제목
st.title("🗺️ 서울 인기 관광지 TOP 10")
st.write("외국인 관광객에게 추천하는 서울의 대표 관광지를 만나보세요.")

# 언어 선택
language = st.radio(
    "언어 선택 / Language",
    ["한국어", "English"],
    horizontal=True
)

english = language == "English"

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커 표시
for p in places:

    name = p["en"] if english else p["name"]
    desc = p["desc_en"] if english else p["desc"]

    popup_text = f"""
    <div style="width:220px">
        <h4>{p['name']}</h4>
        <p>{desc}</p>
    </div>
    """

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{p['name']}",
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color:#2563eb;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                text-align:center;
                line-height:27px;
                font-weight:bold;
                box-shadow:0 1px 5px #777;">
                {places.index(p) + 1}
            </div>
            """
        )
    ).add_to(m)

# 지도 출력
st.subheader("📍 서울 관광지 위치")

st_folium(
    m,
    width=None,
    height=550,
    use_container_width=True
)

# 관광지 설명
st.subheader("🏛️ 서울 관광지 소개")

for i in range(0, len(places), 2):

    col1, col2 = st.columns(2)

    for col, p in zip(
        [col1, col2],
        places[i:i+2]
    ):

        with col:

            name = p["en"] if english else p["name"]
            desc = p["desc_en"] if english else p["desc"]

            with st.container(border=True):

                st.markdown(
                    f"### {places.index(p)+1}. {name}"
                )

                st.write(desc)

                url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    f"{p['lat']},{p['lon']}"
                )

                st.link_button(
                    "Google 지도에서 보기",
                    url,
                    use_container_width=True
                )

st.divider()

st.caption(
    "Map data © OpenStreetMap contributors"
)

st.caption(
    "서울의 대표 관광지를 소개하는 추천 지도입니다."
)
