import os
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
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


data_path = get_absolute_path("./data/cj.png")
main_bg(data_path)


st.write("### 空气质量评估:sunny:")
st.markdown('系统提供1.空气质量与PM2.5简介，2.分省份空气质量查询，3.各省份空气质量对比功能')

st.markdown("""
    #### 1.空气质量与PM2.5简介
    PM2.5是指大气中直径小于或等于2.5微米的颗粒物，也称为细颗粒物。这些微小颗粒能深入肺部甚至血液，对人体健康造成严重影响，是评价空气质量的重要指标之一。
    """)

# 载入数据
air_data_path=get_absolute_path('./data/PM2.5.csv')
# air_data_path = './final_pro/data/PM2.5.csv'
data = pd.read_csv(air_data_path)

st.divider()
st.markdown("#### 2.分省份查询显示空气质量数据：")
st.markdown("请在侧边栏中选择您想查询的省份")


def air():
    # 提示用户选择省份，并将用户选择省份的数据单独提取出来
    column_to_filter = 'province'
    selected_prov_name = st.sidebar.selectbox('选择省/市', data[column_to_filter].unique())
    selected_province_data = data[data[column_to_filter] == selected_prov_name]
    st.write(f"##### 显示省/直辖市：{selected_prov_name}的数据")

    with st.expander("###### 2.1原始数据"):
        # 以dataframe形式显示原始数据
        st.dataframe(selected_province_data.iloc[:, 3:])

    # 用户可单独查询
    years = data.columns[4:].tolist()
    compare = ['>', '<']
    with st.form(key="query"):
        st.markdown("###### 2.2基于属性表达式查询记录")
        selected_year = st.selectbox(label='选择一个查询年份', options=years, index=0, help="请选择一个年份")
        com = st.selectbox(label='选择一个关系', options=compare, index=0, help="请选择判断关系")
        value = st.text_input("输入一个值", help="请输入值")
        submit_button = st.form_submit_button(label="提交")

        if submit_button:
            value = (float(value))  # 转换类型以便后续比较
            if com == "<":
                exp = selected_province_data[selected_year] < value
                new_frame = selected_province_data[exp].iloc[:, 3:]
            else:
                exp = selected_province_data[selected_year] > value
                new_frame = selected_province_data[exp].iloc[:, 3:]
            count = new_frame.shape[0]  # 计数
            st.write("##### 共有" + str(count) + "条数据")
            st.dataframe(new_frame)  # 以dataframe的形式显示子集数据

    # 用户可以选择该省份的一个或者多个地级市，系统将绘制从PM2.5值的年际变化折线图
    with st.form(key='plots'):
        st.markdown("###### 2.3城市空气质量可视化:chart_with_upwards_trend:")
        cities = selected_province_data['city_name'].unique()
        selected_cities = st.multiselect(label='选择一个或多个查询城市', options=cities, default=cities[0],
                                         help="请选择一个或多个城市")
        submit_button = st.form_submit_button(label="确认")

        if submit_button:
            # 绘制折线图
            city_data = selected_province_data[selected_province_data['city_name'].isin(selected_cities)]
            # 创建一个新的数据框，其中包含年份和PM2.5数据
            city_yearly_data = city_data.melt(id_vars=['city_id', 'province', 'city_code', 'city_name'],
                                              var_name='year',
                                              value_name='PM2.5')
            fig = px.line(city_yearly_data, x='year', y='PM2.5', color='city_name', title=f'选定城市的PM2.5年际变化')
            fig.update_layout(xaxis_title='年份', yaxis_title='PM2.5值')
            st.plotly_chart(fig)

    # 以热力图的形式，空间上直观地呈现各省份空气质量对比
    st.divider()
    st.markdown("#### 3.各省份空气质量可视化对比：")
    with st.form(key='heatmap'):
        st.markdown("###### 各省份空气质量热力图")
        selected_year_for_heatmap = st.selectbox(label='选择一个年份', options=years, index=0, help="请选择一个年份")
        submit_button = st.form_submit_button(label="确认")

        if submit_button:
            province_data=get_absolute_path('./data/pm2.5_province.csv')
            pro_data = pd.read_csv(province_data)
            province_avg_pm25 = pro_data[['province', 'lon', 'lat', selected_year_for_heatmap]].copy()
            province_avg_pm25.columns = ['province', 'lon', 'lat', 'average_PM2.5']

            # 创建地图，添加热力图层
            m = folium.Map(location=[35.8617, 104.1954], zoom_start=4, tiles='Gaode.Normal')
            heat_data = [[row['lat'], row['lon'], row['average_PM2.5']] for index, row in province_avg_pm25.iterrows()]
            HeatMap(heat_data).add_to(m)
            folium_static(m)


air()
