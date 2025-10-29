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
#             第二部分：台南 DEM 模擬
# ===============================================
st.title("🏞️ Pydeck 3D 地圖 (網格 - 台南 DEM 模擬)")

# --- 1. 載入 DEM CSV 資料 ---
df_dem = pd.read_csv("tainan_dem.csv")

# 確保欄位名稱一致
df_dem.rename(columns={
    "Longitude": "lon",
    "Latitude": "lat",
    "Elevation": "elevation"
}, inplace=True)

st.write("📊 台南 DEM 資料預覽", df_dem.head())

# --- 2. 設定 GridLayer ---
layer_grid = pdk.Layer(
    'GridLayer',
    data=df_dem,
    get_position='[lon, lat]',
    get_elevation_weight='elevation',
    elevation_scale=1,
    cell_size=2000,
    extruded=True,
    pickable=True
)

# --- 3. 設定視角 ---
view_state_grid = pdk.ViewState(
    latitude=df_dem["lat"].mean(),
    longitude=df_dem["lon"].mean(),
    zoom=12,
    pitch=50
)

# --- 4. 顯示地圖 ---
r_grid = pdk.Deck(
    layers=[layer_grid],
    initial_view_state=view_state_grid,
    tooltip={"text": "海拔高度: {elevationValue} 公尺"}
)
st.pydeck_chart(r_grid)
