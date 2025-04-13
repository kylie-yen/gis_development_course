import os
import streamlit as st
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_folium import st_folium
import base64


def main_bg(temp):
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(temp, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


def get_absolute_path(relative_path):
    # 获取当前脚本的绝对路径
    dir_of_this_script = os.path.dirname(os.path.abspath(__file__))
    # 构建到目标文件的绝对路径
    return os.path.join(dir_of_this_script, relative_path)


background_path = get_absolute_path("./data/cj.png")
main_bg(background_path)


st.write("### 风景名胜")

st.markdown("""
    各类自然、文化景观作为大自然的杰作与人类文明的瑰宝，不仅构成了地球多样而绚烂的面貌，也深刻影响着人们的精神世界和文化认同。它们如同历史的活化石，承载着丰富的自然生态信息和人文故事，让现代人在快节奏的生活中得以寻觅到一份宁静与启迪。
    
    自然风光的壮丽，如高山峻岭、江河湖海、幽谷飞瀑，不仅能激发人们对美的无限向往和创造力，还能在心灵层面提供慰藉，帮助缓解压力，促进心理健康。而文化景观，如古迹遗址、传统村落、宗教圣地等，则是人类智慧与历史进程的见证，它们通过一砖一瓦、一草一木讲述着过往的辉煌与沧桑，增进人们对不同文化的理解和尊重，促进社会的和谐共存。
    
    人们旅行出游的主要目的地也大多为各类风景名胜，或打开古代分流人物居所，或亲近自然。
    """)

st.markdown('请在侧边栏中选择想要查询的风景名胜类型，系统将呈现各省市的风景名胜数目，点击省份可以看到更详细的信息')

# 载入数据
data_path=get_absolute_path('./data/scenery.csv')
df = pd.read_csv(data_path, encoding='utf-8')

# 将列名从Index转换为列表
scen_spot_types = df.columns[3:]
scen_spot_types_list = scen_spot_types.tolist()

# 侧边栏选项
selected_types = st.sidebar.multiselect('选择风景名胜类型:church:', scen_spot_types_list, default=scen_spot_types_list)
filtered_df = df[df[selected_types].sum(axis=1) > 0]

# 创建基于高德地图的Folium地图
map_center = [30, 106.5]
my_map = folium.Map(location=map_center, zoom_start=5, control_scale=True, tiles='Gaode.Normal')

# 各省风景名胜点添加
marker_cluster = MarkerCluster().add_to(my_map)

for _, row in filtered_df.iterrows():
    for spot_type in selected_types:
        if row[spot_type]:
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"{row['province']} - {spot_type}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)

# 展示地图
st_folium(my_map, width=700, height=500)
