import os
import streamlit as st
import folium
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import datetime
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

st.write("### 安全性")

st.markdown("""
    地震作为一种极具破坏力的自然灾害，其危害体现在多个层面，从直接的物理破坏到深远的社会经济影响。大型地震带给城市的伤痛需要很长时间弥合。
    
    直接灾害包括地面断裂、建筑物倒塌，导致人员伤亡、家庭破碎，基础设施受损，如道路中断、桥梁垮塌，严重影响救援效率和灾后恢复。次生灾害随之而来，如山体滑坡、泥石流切断交通，水库大坝受损引发洪水，火灾因燃气泄漏或电力设施损坏而难以控制，甚至可能引爆化学危险品，加剧灾难程度。
    
    此外，地震还可能污染水源，增加瘟疫流行的风险，对生态环境造成长期伤害。经济活动受阻，教育、卫生系统受损，心理健康问题凸显，这些都是地震带来的深刻社会影响。
    
    我们需要保留对过去灾难的记忆，警示未来，在不可预知的地震面前，最大限度保障生命安全和社会稳定。
    """)

st.markdown(
    '请在侧边栏中选择时间范围，系统将呈现这段时间范围内各省市的历史地震数据，点击各点可以看到更详细的信息，包括震级、震源深度、发生时间等')

# 设置Streamlit页面标题和侧边栏
st.markdown('##### 地震数据可视化')
st.write("绿色：震级<4   橘色：4<震级<6   红色：震级>6")
st.sidebar.title('时间范围选择')

# 加载地震数据
shp_path = get_absolute_path('./data/earthquake.shp')
earthquakes = gpd.read_file(shp_path)

# 时间格式，包括小数秒
fmt = '%Y/%m/%dT%H:%M:%S.%f'
earthquakes['OT'] = pd.to_datetime(earthquakes['OT'], format=fmt, errors='coerce')

# 时间选择输入
start_date = earthquakes['OT'].min()
end_date = earthquakes['OT'].max()
selected_start_date = st.sidebar.date_input('选择开始日期', value=start_date, min_value=start_date, max_value=end_date)
selected_end_date = st.sidebar.date_input('选择结束日期', value=end_date, min_value=start_date, max_value=end_date)

# 转换为datetime对象
selected_start_date = datetime.datetime.combine(selected_start_date, datetime.datetime.min.time())
selected_end_date = datetime.datetime.combine(selected_end_date, datetime.datetime.max.time())

# 过滤数据
filtered_earthquakes = earthquakes[
    (earthquakes['OT'] >= selected_start_date) & (earthquakes['OT'] <= selected_end_date)]

# 创建基于高德地图的Folium地图
map_center = [30, 106.5]
mymap = folium.Map(location=map_center, zoom_start=5, control_scale=True, tiles='Gaode.Normal')


# 根据地震级别设置图标大小和颜色
def get_marker_icon(magnitude):
    if magnitude < 4.0:
        return folium.Icon(icon='cloud', color='green')
    elif magnitude < 6.0:
        return folium.Icon(icon='cloud', color='orange')
    else:
        return folium.Icon(icon='cloud', color='red')


# 添加地震点到地图上
for idx, row in filtered_earthquakes.iterrows():
    popup_text = f"发生时间: {row['OT']}<br>深度: {row['DEPTH']} km<br>震级: {row['MAGNITUDE']} {row['MAGTYPE']}<br>地点: {row['REGION']}"
    folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=popup_text, icon=get_marker_icon(row['MAGNITUDE'])).add_to(
        mymap)

# 在Streamlit页面上显示地图
folium_static(mymap)
st.markdown("---")
st.write("选择的时间范围:", selected_start_date, "到", selected_end_date)
st.write(f"显示了 {len(filtered_earthquakes)} 个地震事件。")
