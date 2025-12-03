import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="Taxi Finder", page_icon="🚖")

st.title("🚖 전시장 택시 승강장 안내")
st.write("관람하고 계신 **전시장**을 선택해주세요.")

# --- 데이터: 주요 전시장 및 택시 승강장 좌표 (위도, 경도) ---
# 실무에서는 이 좌표를 더 정확하게 찍어주시면 됩니다.
venues = {
    "COEX (서울 삼성동)": {
        "center": [37.5118, 127.0593], # 코엑스 중심
        "taxi": [37.5125, 127.0588],   # 동문 앞 택시 승강장 (예시)
        "desc": "코엑스 동문 앞 대로변"
    },
    "KINTEX 제1전시장 (일산)": {
        "center": [37.6690, 126.7460],
        "taxi": [37.6695, 126.7475],   # 1전시장 앞 승강장
        "desc": "제1전시장 3번 게이트 앞"
    },
    "KINTEX 제2전시장 (일산)": {
        "center": [37.6645, 126.7410],
        "taxi": [37.6640, 126.7405],
        "desc": "제2전시장 7번 게이트 앞"
    },
    "BEXCO (부산)": {
        "center": [35.1691, 129.1360],
        "taxi": [35.1695, 129.1365],
        "desc": "제1전시장 정문 앞 광장"
    }
}

# --- UI: 전시장 선택 ---
selected_venue_name = st.selectbox("어디에 계신가요?", list(venues.keys()))
venue_data = venues[selected_venue_name]

# --- 정보 표시 ---
st.success(f"📍 **택시 타는 곳:** {venue_data['desc']}")

# --- 지도 시각화 (Folium) ---
# 지도 중심 설정
m = folium.Map(location=venue_data["center"], zoom_start=17)

# 1. 전시장 위치 마커 (파란색)
folium.Marker(
    venue_data["center"],
    popup=selected_venue_name,
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# 2. 택시 승강장 위치 마커 (빨간색)
folium.Marker(
    venue_data["taxi"],
    popup="택시 승강장",
    icon=folium.Icon(color="red", icon="taxi", prefix='fa')
).add_to(m)

# 지도 그리기
st_data = st_folium(m, width=700, height=400)

# --- 실전 기능: 길찾기 버튼 (앱 연동) ---
st.markdown("### 🏃‍♂️ 길찾기 앱으로 바로 연결")
col1, col2 = st.columns(2)

taxi_lat = venue_data['taxi'][0]
taxi_lng = venue_data['taxi'][1]

# 네이버지도/카카오맵 URL 스키마 활용
# 모바일에서 클릭 시 앱이 열리거나 웹지도로 연결됩니다.
naver_map_url = f"https://map.naver.com/v5/directions/-/-/{taxi_lng},{taxi_lat},택시승강장/-/walk"
kakao_map_url = f"https://map.kakao.com/link/to/택시승강장,{taxi_lat},{taxi_lng}"

with col1:
    st.link_button("🟢 네이버 지도로 길찾기", naver_map_url, use_container_width=True)

with col2:
    st.link_button("🟡 카카오맵으로 길찾기", kakao_map_url, use_container_width=True)

st.info("👆 위 버튼을 누르면 현재 위치에서 승강장까지의 **도보 경로**가 안내됩니다.")
