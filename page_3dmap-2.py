import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("互動式 3D 地圖展示 (20 個國家)")

# ==============================
# 1️⃣ 3D 地球儀 (20 個真實國家)
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

with st.expander("3D 地球儀 (20 國家)"):
    fig_geo = px.scatter_geo(
        df_geo,
        locations="iso_alpha",
        color="continent",
        hover_name="country",
        size="pop",
        projection="orthographic"
    )
    st.plotly_chart(fig_geo, use_container_width=True)

# ==============================
# 2️⃣ 模擬 DEM Surface 資料
# ==============================
x_size, y_size = 50, 50
x = np.linspace(-3, 3, x_size)
y = np.linspace(-3, 3, y_size)
X, Y = np.meshgrid(x, y)
Z = np.exp(-X**2 - Y**2) * 1000  # 模擬山峰
Z += np.random.rand(x_size, y_size) * 50  # 隨機起伏

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
