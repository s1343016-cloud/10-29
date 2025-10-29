import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests

st.title("互動式 3D 地圖展示：地球儀 + 火山")

# ==============================
# 1️⃣ 國家點資料
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
lat = [23.7, 38.9, 35.9, 46.2, -14.2, -25.3, 20.6, 36.0, 51.2, -30.6,
       61.5, 56.1, 23.6, 41.9, 40.4, 26.8, -38.4, 36.5, 55.4, 24.7]
lon = [121.0, -77.0, 104.1, 2.2, -51.9, 133.8, 78.9, 138.2, 10.4, 22.9,
       105.3, -106.3, -102.5, 12.6, -3.7, 30.8, -64.2, 127.8, -3.4, 46.7]

R = 1
lat_rad = np.radians(lat)
lon_rad = np.radians(lon)
x = R * np.cos(lat_rad) * np.cos(lon_rad)
y = R * np.cos(lat_rad) * np.sin(lon_rad)
z = R * np.sin(lat_rad)

df_geo = pd.DataFrame({
    "country": countries,
    "continent": continents,
    "pop": pop,
    "x": x,
    "y": y,
    "z": z
})

# ==============================
# 2️⃣ 讀取各洲 GeoJSON
# ==============================
url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
geojson = requests.get(url).json()

continent_colors = {
    "Asia": "orange",
    "Europe": "green",
    "Africa": "yellow",
    "Americas": "blue",
    "Oceania": "purple"
}

# ==============================
# 3️⃣ 球體地球儀 + 各洲輪廓 + 國家點
# ==============================
fig_sphere = go.Figure()

# 球面
u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
xs = R * np.cos(u) * np.sin(v)
ys = R * np.sin(u) * np.sin(v)
zs = R * np.cos(v)
fig_sphere.add_trace(go.Surface(
    x=xs, y=ys, z=zs,
    colorscale=[[0, 'lightblue'], [1, 'lightblue']],
    opacity=0.5,
    showscale=False
))

# 國家點
fig_sphere.add_trace(go.Scatter3d(
    x=df_geo["x"], y=df_geo["y"], z=df_geo["z"],
    mode='markers+text',
    marker=dict(size=np.log(df_geo["pop"])/2, color='red'),
    text=df_geo["country"],
    textposition="top center"
))

# 經緯度轉 XYZ
def latlon_to_xyz(lat, lon, radius=1.001):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return x, y, z

# 各洲輪廓
for feature in geojson["features"]:
    props = feature["properties"]
    continent = props.get("CONTINENT", "Asia")
    geom_type = feature["geometry"]["type"]
    coords = feature["geometry"]["coordinates"]

    if geom_type == "Polygon":
        for poly in coords:
            lon_poly, lat_poly = zip(*poly)
            xs, ys, zs = latlon_to_xyz(lat_poly, lon_poly)
            fig_sphere.add_trace(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode='lines',
                line=dict(color=continent_colors.get(continent, "white"), width=2),
                showlegend=False
            ))
    elif geom_type == "MultiPolygon":
        for multipoly in coords:
            for poly in multipoly:
                lon_poly, lat_poly = zip(*poly)
                xs, ys, zs = latlon_to_xyz(lat_poly, lon_poly)
                fig_sphere.add_trace(go.Scatter3d(
                    x=xs, y=ys, z=zs,
                    mode='lines',
                    line=dict(color=continent_colors.get(continent, "white"), width=2),
                    showlegend=False
                ))

fig_sphere.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        aspectmode='data'
    ),
    height=700,
    title="3D 球體地球儀 + 各洲輪廓 + 國家點"
)

st.plotly_chart(fig_sphere, use_container_width=True)

# ==============================
# 4️⃣ 改良版富士山火山 DEM + 高度滑桿
# ==============================
height_scale = st.slider("調整高度比例", 0.1, 3.0, 1.0, 0.1)

x_size, y_size = 100, 100
x = np.linspace(-3, 3, x_size)
y = np.linspace(-3, 3, y_size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# 底部寬錐
# 底部寬錐
n = 2.0
Z_base = np.maximum(0, (1 - R)**n) * 1000

# 頂部略平
Z_top = np.exp(-R**2 / 0.08) * 150  # 高度小帽，不要火山口

# 自然起伏
Z_noise = np.random.rand(x_size, y_size) * 20

# 最終高度
Z = (Z_base + Z_top + Z_noise) * height_scale


fig_surface = go.Figure(
    data=[
        go.Surface(
            z=Z,
            colorscale="Viridis",
            showscale=True,
            lighting=dict(ambient=0.6, diffuse=0.8, specular=0.5),
            contours={"z": {"show": True, "start": 200, "end": 1000*height_scale, "size": 100}}
        )
    ]
)

fig_surface.update_layout(
    title=" 3D 火山地形",
    width=800,
    height=700,
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='高度 (Z)'
    )
)

st.plotly_chart(fig_surface, use_container_width=True)
