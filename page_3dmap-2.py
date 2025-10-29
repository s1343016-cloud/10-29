import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("互動式 3D 地圖展示")

# ==============================
# 1️⃣ Mapbox 衛星地球儀 (20 國家)
# ==============================
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

pop = [
    23_000_000, 330_000_000, 1_400_000_000, 67_000_000, 211_000_000, 25_000_000,
    1_380_000_000, 126_000_000, 83_000_000, 59_000_000, 146_000_000, 38_000_000,
    128_000_000, 60_000_000, 47_000_000, 104_000_000, 45_000_000, 52_000_000,
    67_000_000, 35_000_000
]

# 經緯度 (近似城市座標)
lat = [23.7, 38.9, 35.9, 46.2, -14.2, -25.3, 20.6, 36.0, 51.2, -30.6,
       61.5, 56.1, 23.6, 41.9, 40.4, 26.8, -38.4, 36.5, 55.4, 24.7]
lon = [121.0, -77.0, 104.1, 2.2, -51.9, 133.8, 78.9, 138.2, 10.4, 22.9,
       105.3, -106.3, -102.5, 12.6, -3.7, 30.8, -64.2, 127.8, -3.4, 46.7]

df_geo = pd.DataFrame({
    "country": countries,
    "continent": continents,
    "pop": pop,
    "lat": lat,
    "lon": lon
})

mapbox_token = "YOUR_MAPBOX_TOKEN"  # <- 換成你的 Mapbox token
px.set_mapbox_access_token(mapbox_token)

with st.expander("3D 地球儀 (Mapbox 衛星底圖)"):
    fig_geo = px.scatter_mapbox(
        df_geo,
        lat="lat",
        lon="lon",
        color="continent",
        size="pop",
        hover_name="country",
        zoom=0,
        height=600,
        mapbox_style="satellite"
    )
    st.plotly_chart(fig_geo, use_container_width=True)

# ==============================
# 2️⃣ 模擬 DEM 3D 火山地形
# ==============================
x_size, y_size = 50, 50
x = np.linspace(-3, 3, x_size)
y = np.linspace(-3, 3, y_size)
X, Y = np.meshgrid(x, y)
Z = np.exp(-X**2 - Y**2) * 1000      # 模擬高斯山峰
Z += np.random.rand(x_size, y_size) * 50  # 加隨機起伏

with st.expander("3D 模擬火山地形"):
    fig_surface = go.Figure(
        data=[
            go.Surface(
                z=Z,
                colorscale="Viridis",
                showscale=True,
                lighting=dict(ambient=0.6, diffuse=0.8, specular=0.5),
                contours={"z": {"show": True, "start": 200, "end": 1000, "size": 100}}
            )
        ]
    )

    fig_surface.update_layout(
        title="模擬火山 3D 地形圖",
        width=800,
        height=700,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='高度 (Z)'
        )
    )

    st.plotly_chart(fig_surface, use_container_width=True)
