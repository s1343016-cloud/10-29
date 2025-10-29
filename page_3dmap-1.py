import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# ===============================================
#             第一部分：彰化熱度圖
# ===============================================
st.title("🌇 Pydeck 3D 地圖 (向量 - 彰化熱度圖)")

# 0. 檢查 Mapbox 金鑰是否存在於 Secrets 中
if "MAPBOX_API_KEY" not in st.secrets:
    st.error("Mapbox API Key (名稱需為 MAPBOX_API_KEY) 未設定！請在雲端 Secrets 中設定。")
    st.stop()

# --- 1. 生成範例資料（模擬彰化市隨機點） ---
# 彰化市中心大約位置：經度 120.541, 緯度 24.074
data = pd.DataFrame({
    'lat': 24.074 + np.random.randn(1000) / 80,  # 緯度隨機擴散
    'lon': 120.541 + np.random.randn(1000) / 80, # 經度隨機擴散
})

# --- 2. 設定 HexagonLayer ---
layer_hexagon = pdk.Layer(
    'HexagonLayer',
    data=data,
    get_position='[lon, lat]',
    radius=120,
    elevation_scale=5,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# --- 3. 設定視角 ---
view_state_hexagon = pdk.ViewState(
    latitude=24.074,
    longitude=120.541,
    zoom=12,
    pitch=50,
)

# --- 4. 顯示地圖 ---
r_hexagon = pdk.Deck(
    layers=[layer_hexagon],
    initial_view_state=view_state_hexagon,
    tooltip={"text": "這個區域有 {elevationValue} 個熱點"}
)
st.pydeck_chart(r_hexagon)


# ===============================================
#          第二個地圖：模擬台南 DEM
# ===============================================

st.title("Pydeck 3D 地圖 (網格 - 台南 DEM 模擬)")

# --- 1. 模擬 DEM 網格資料 ---
x, y = np.meshgrid(np.linspace(-1, 1, 50), np.linspace(-1, 1, 50))
z = np.exp(-(x**2 + y**2) * 2) * 800 + np.random.rand(50, 50) * 200  # 模擬地形起伏

data_dem_list = []
base_lat, base_lon = 23.0, 120.2  # 台南中心位置
for i in range(50):
    for j in range(50):
        data_dem_list.append({
            "lon": base_lon + x[i, j] * 0.15,
            "lat": base_lat + y[i, j] * 0.15,
            "elevation": z[i, j]
        })
df_dem = pd.DataFrame(data_dem_list)

# --- 2. 設定 Pydeck 圖層 (GridLayer) ---
layer_grid = pdk.Layer(
    "GridLayer",
    data=df_dem,
    get_position='[lon, lat]',
    get_elevation_weight="elevation",
    elevation_scale=1,
    cell_size=2000,
    extruded=True,
    pickable=True
)

# --- 3. 設定視角 (View) ---
view_state_grid = pdk.ViewState(
    latitude=base_lat, longitude=base_lon, zoom=9.5, pitch=50
)

# --- 4. 組合並顯示 ---
r_grid = pdk.Deck(
    layers=[layer_grid],
    initial_view_state=view_state_grid,
    tooltip={"text": "海拔高度: {elevationValue} 公尺"}
)
st.pydeck_chart(r_grid)
