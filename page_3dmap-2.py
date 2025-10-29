import streamlit as st
import plotly.express as px
import pandas as pd

st.title("3D 地球儀 (Mapbox 衛星底圖)")

# --- 20 個真實國家資料 ---
countries = [
    "Taiwan", "USA", "China", "France", "Brazil", "Australia", "India", "Japan",
    "Germany", "South Africa", "Russia", "Canada", "Mexico", "Italy", "Spain",
    "Egypt", "Argentina", "South Korea", "UK", "Saudi Arabia"
]

continents = [
    "Asia", "Americas", "Asia", "Europe", "Americas", "Oceania", "Asia", "Asia",
    "Europe", "Africa", "Europe", "Americas", "Americas", "Europe", "Europe",
    "Africa", "Americas", "Asia", "Europe", "Asia"
]

iso_alpha = [
    "TWN", "USA", "CHN", "FRA", "BRA", "AUS", "IND", "JPN",
    "DEU", "ZAF", "RUS", "CAN", "MEX", "ITA", "ESP",
    "EGY", "ARG", "KOR", "GBR", "SAU"
]

pop = [
    23_000_000, 330_000_000, 1_400_000_000, 67_000_000, 211_000_000, 25_000_000,
    1_380_000_000, 126_000_000, 83_000_000, 59_000_000, 146_000_000, 38_000_000,
    128_000_000, 60_000_000, 47_000_000, 104_000_000, 45_000_000, 52_000_000,
    67_000_000, 35_000_000
]

df_geo = pd.DataFrame({
    "country": countries,
    "continent": continents,
    "iso_alpha": iso_alpha,
    "pop": pop
})

# --- 使用 Mapbox 衛星底圖 ---
mapbox_token = "pk.eyJ1IjoiczEzNDMwMTYiLCJhIjoiY21oYmJkZGJ5MHdxZDJqcHg1NWk2NGp5MyJ9.HqfgX8ODaAUpLIWV3R2TQg"  # <- 換成你的 Mapbox token

px.set_mapbox_access_token(mapbox_token)

fig_geo = px.scatter_mapbox(
    df_geo,
    lat=[23.7, 38.9, 35.9, 46.2, -14.2, -25.3, 20.6, 36.0, 51.2, -30.6,
         61.5, 56.1, 23.6, 41.9, 40.4, 26.8, -38.4, 36.5, 55.4, 24.7],  # 緯度
    lon=[121.0, -77.0, 104.1, 2.2, -51.9, 133.8, 78.9, 138.2, 10.4, 22.9,
         105.3, -106.3, -102.5, 12.6, -3.7, 30.8, -64.2, 127.8, -3.4, 46.7], # 經度
    color="continent",
    size="pop",
    hover_name="country",
    zoom=0,
    height=600,
    mapbox_style="satellite"
)

st.plotly_chart(fig_geo, use_container_width=True)
