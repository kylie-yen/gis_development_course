import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import requests
from io import BytesIO
from folium.plugins import MousePosition


@st.cache_data(ttl=3600)
def load_geojson(url):
    response = requests.get(url)
    gdf = gpd.read_file(BytesIO(response.content))
    return gdf


url = "https://EcnuGISChaser.github.io/gis_development/data/tms_POIs.geojson"
gdf = load_geojson(url)  # 加载数据


def create_marker(feature):
    name = feature.get('NAME', '未知名称')
    text = feature.get('text', '')
    photo_url = feature.get('photo_url', None)
    popup_content = f"""
    <h4>{name}</h4>
    <h6>{text}</h6>
    <img src={photo_url}>
    """
    folium.Marker(location=[feature.geometry.y, feature.geometry.x],popup=folium.Popup(popup_content, max_width=300)).add_to(marker_cluster)


# 计算地图的初始范围并初始化Map控件
bounds = gdf.bounds
map_center = [(bounds['miny'].min() + bounds['maxy'].max()) / 2, (bounds['minx'].min() + bounds['maxx'].max()) / 2]
m = folium.Map(location=map_center, zoom_start=13, tiles=None)

# 为每个点添加标记
marker_cluster = folium.FeatureGroup(name="POI").add_to(m)
for idx, feature in gdf.iterrows():
    create_marker(feature)

# 添加Tile图层
tiles_list = {
    "ESRI全球影像": {"tiles": "Esri.WorldImagery", "name": "ESRI全球影像", "control": True, "overlay": False},
    "Carto地图": {"tiles": "CartoDB.Positron", "name": "Carto地图", "control": True, "overlay": False},
    "高德地图": {"tiles": "Gaode.Normal", "name": "高德地图", "control": True, "overlay": False}
}

for name, params in tiles_list.items():
    folium.TileLayer(tiles=params["tiles"], name=params["name"], control=params["control"],overlay=params["overlay"]).add_to(m)

# 鼠标位置
mouse_position = MousePosition(position='bottomright', separator=' : ')
mouse_position.add_to(m)

folium.LayerControl().add_to(m)  # 添加图层控制控件，此时tiles会自动归类为base layer，而之前添加的POI为overlay
st.title("天目山野外实习区域POI地图")
folium_static(m, width=800, height=600)
