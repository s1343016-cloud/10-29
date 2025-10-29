import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("互動式 3D 地圖展示")

# ==============================
# 1️⃣ 模擬 3D 地球儀資料
# ==============================
# 模擬 20 個國家資料
np.random.seed(42)
countries = [f"Country {i}" for i in range(1, 21)]
continents = ["Asia", "Europe", "Africa", "Americas", "Oceania"]
iso_alpha = [f"C{i:03}" for i in range(1, 21)]

df_geo = pd.DataFrame({
    "country": countries,
    "continent": np.random.choice(continents, size=20),
    "iso_alpha": iso_alpha,
    "pop": np.random.randint(1_000_000, 300_000_000, size=20)
})

with st.expander("3D 地球儀 (模擬資料)"):
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
# 模擬 50x50 的高程數據 (隨機 + 高斯峰)
x_size, y_size = 50, 50
x = np.linspace(-3, 3, x_size)
y = np.linspace(-3, 3, y_size)
X, Y = np.meshgrid(x, y)
Z = np.exp(-X**2 - Y**2) * 1000  # 模擬一個山峰
Z += np.random.rand(x_size, y_size) * 50  # 加一些隨機起伏

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
