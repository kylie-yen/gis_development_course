import streamlit as st
import fiona
from shapely.geometry import Point

st.write('10214507042 阎格:sparkles:')
schema = {'geometry': 'Point','properties': {'城市名': 'str:254', '经度': 'float:19.11', '纬度': 'float:19.11', '省名': 'str:254'}}
with fiona.open('china_cities_prj.shp', encoding='utf-8', driver='ESRI Shapefile', schema=schema) as shp_data:
    with st.form(key="my_form"):
        st.markdown("### 查询周边城市")
        selected_city_name = st.selectbox(label='选择一个城市', options=[city['properties']['城市名'] for city in shp_data],index=0, help="请选择一个城市")
        distance_km = st.number_input(label='输入邻近距离（0-1000）', min_value=0, max_value=1000, value=300, step=1, help="请输入距离")
        show_nearest = st.checkbox(label='显示最近城市与距离', value=False, key=None,help='勾选将显示最近的城市及其距离', on_change=None)
        submit_button = st.form_submit_button(label="查询")

    if submit_button:  # 用户点击查询按钮
        nearby_city = {}  # 建立字典，存储{城市名称：距离}
        selected_city = next((city for city in shp_data if city['properties']['城市名'] == selected_city_name))  # 使用next方法找到用户选择的城市
        for city in shp_data:
            dis = Point(selected_city['geometry']['coordinates']).distance(Point(city['geometry']['coordinates']))  # 计算每一个城市与用户选择的城市的距离
            if dis <= (distance_km * 1000) and city['properties']['城市名'] != selected_city_name:
                nearby_city[f'{city['properties']['城市名']}'] = dis  # 小于用户给定的距离就存储到字典里

        st.write(f"周边城市数量: {len(nearby_city)}")  # 输出距离范围内的城市数量
        for key in nearby_city.keys():
            st.write(key)  # 输出各城市名称

        if show_nearest:  # 输出距离最近的城市名称及其距离
            try:
                nearest_cityname = min(nearby_city, key=nearby_city.get)
                min_distance_km = nearby_city[nearest_cityname] / 1000
                st.write(f'最近的城市是{nearest_cityname}，距离为{min_distance_km:.2f}公里')
            except ValueError:
                st.write("当前搜索半径过小！请调整搜索半径！")
shp_data.close()
