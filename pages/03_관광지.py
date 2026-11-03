
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="스위스 관광지 여행",
    page_icon="🏔️",
    layout="wide"
)

# ==========================
# 스위스 관광지 데이터
# ==========================

places = [
    {
        "day": "DAY 1",
        "time": "오전",
        "name": "취리히 구시가지",
        "lat": 47.3769,
        "lon": 8.5417,
        "desc": "리마트강 주변의 아름다운 중세 골목과 역사적인 건축물을 둘러봅니다."
    },
    {
        "day": "DAY 1",
        "time": "오후",
        "name": "루체른 카펠교",
        "lat": 47.0510,
        "lon": 8.3070,
        "desc": "스위스에서 유명한 목조 다리와 아름다운 호수 풍경을 감상합니다."
    },
    {
        "day": "DAY 1",
        "time": "저녁",
        "name": "루체른 호수",
        "lat": 47.0520,
        "lon": 8.3190,
        "desc": "산으로 둘러싸인 호수에서 아름다운 저녁 풍경을 즐깁니다."
    },
    {
        "day": "DAY 2",
        "time": "오전",
        "name": "인터라켄",
        "lat": 46.6863,
        "lon": 7.8632,
        "desc": "툰 호수와 브리엔츠 호수 사이에 있는 아름다운 관광도시입니다."
    },
    {
        "day": "DAY 2",
        "time": "오후",
        "name": "라우터브루넨",
        "lat": 46.5935,
        "lon": 7.9091,
        "desc": "아름다운 폭포와 알프스 산맥으로 유명한 마을입니다."
    },
    {
        "day": "DAY 2",
        "time": "저녁",
        "name": "그린델발트",
        "lat": 46.6242,
        "lon": 8.0414,
        "desc": "아이거 북벽과 아름다운 알프스 풍경을 감상할 수 있습니다."
    },
    {
        "day": "DAY 3",
        "time": "종일",
        "name": "융프라우요흐",
        "lat": 46.5475,
        "lon": 7.9850,
        "desc": "알프스의 아름다운 설산과 빙하를 감상할 수 있는 전망대입니다."
    },
    {
        "day": "DAY 4",
        "time": "오전",
        "name": "체르마트",
        "lat": 46.0207,
        "lon": 7.7491,
        "desc": "스위스의 상징인 마터호른 산으로 유명한 산악 마을입니다."
    },
    {
        "day": "DAY 4",
        "time": "오후",
        "name": "고르너그라트",
        "lat": 45.9830,
        "lon": 7.7840,
        "desc": "산악열차를 타고 올라가 마터호른과 주변 산을 감상합니다."
    },
    {
        "day": "DAY 5",
        "time": "오전",
        "name": "몽트뢰",
        "lat": 46.4312,
        "lon": 6.9107,
        "desc": "레만호 주변의 아름다운 호숫가와 산책로를 즐깁니다."
    },
    {
        "day": "DAY 5",
        "time": "오후",
        "name": "시옹성",
        "lat": 46.4142,
        "lon": 6.9270,
        "desc": "레만호 물가에 세워진 아름다운 중세 시대의 성입니다."
    },
    {
        "day": "DAY 5",
        "time": "저녁",
        "name": "베른 구시가지",
        "lat": 46.9479,
        "lon": 7.4474,
        "desc": "유네스코 세계유산으로 지정된 역사적인 구시가지입니다."
    }
]

# ==========================
# 제목
# ==========================

st.title("🏔️ 스위스 관광지 여행 플래너")

st.write(
    "스위스의 아름다운 관광지를 지도에서 확인하고 "
    "5일 여행 일정을 계획해 보세요."
)

# 언어 선택
language = st.radio(
    "언어 선택",
    ["한국어", "English"],
    horizontal=True
)

# ==========================
# 지도 생성
# ==========================

st.subheader("📍 스위스 관광지 전체 지도")

m = folium.Map(
    location=[46.65, 8.05],
    zoom_start=7,
    tiles="OpenStreetMap"
)

colors = {
    "DAY 1": "blue",
    "DAY 2": "green",
    "DAY 3": "red",
    "DAY 4": "purple",
    "DAY 5": "orange"
}

for i, p in enumerate(places, start=1):

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=p["name"],
        popup=folium.Popup(
            f"""
            <b>{p['name']}</b><br>
            {p['day']} - {p['time']}<br>
            {p['desc']}
            """,
            max_width=300
        ),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:{colors[p['day']]};
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                text-align:center;
                line-height:27px;
                font-weight:bold;
                box-shadow:0 1px 5px #777;">
                {i}
            </div>
            """
        )
    ).add_to(m)

# 지도 출력
st_folium(
    m,
    width=None,
    height=560,
    use_container_width=True
)

st.caption(
    "지도 번호는 아래 관광지 일정과 연결됩니다."
)

# ==========================
# 여행 일정
# ==========================

st.divider()

st.title("🗓️ 스위스 5일 여행 일정")

selected_day = st.selectbox(
    "여행 날짜 선택",
    [
        "전체 일정",
        "DAY 1",
        "DAY 2",
        "DAY 3",
        "DAY 4",
        "DAY 5"
    ]
)

for day in ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]:

    if selected_day != "전체 일정" and selected_day != day:
        continue

    daily_places = [
        p for p in places
        if p["day"] == day
    ]

    st.header(day)

    for i, p in enumerate(places, start=1):

        if p["day"] != day:
            continue

        with st.container(border=True):

            col1, col2 = st.columns([1, 4])

            with col1:
                st.markdown(f"### {p['time']}")

            with col2:
                st.subheader(p["name"])
                st.write(p["desc"])

                url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    f"{p['lat']},{p['lon']}"
                )

                st.link_button(
                    "📍 Google 지도에서 위치 보기",
                    url
                )

# ==========================
# 여행 안내
# ==========================

st.divider()

st.title("✈️ 스위스 여행 안내")

st.markdown("""
### 여행 전 확인 사항

- 산악열차와 케이블카는 날씨와 계절에 따라 운행이 달라집니다.
- 융프라우요흐 방문 전 기상 상황을 확인하세요.
- 체르마트는 일반 차량 진입이 제한되는 지역입니다.
- 스위스는 지역 간 이동에 시간이 걸리므로 열차 시간을 미리 확인하세요.
- 숙박 장소와 이동 순서를 여행 기간에 맞게 조정하세요.
""")

st.caption(
    "지도 데이터 © OpenStreetMap contributors"
)

st.caption(
    "스위스 관광지 추천 여행 일정"
)
