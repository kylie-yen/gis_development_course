import os
import folium
import streamlit as st
from folium.plugins import MousePosition
from streamlit_folium import folium_static
import base64


def main_bg(temp):
    """
    设置一张照片为streamlit网页的背景
    """
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


def changjiang_map():
    """
    定义长江流域的经纬度范围并计算地图的中心点,创建地图
    """
    min_lat, max_lat, min_lon, max_lon = 24.0, 36.0, 90.0, 123.0
    center_lat, center_lon = (min_lat + max_lat) / 2, (min_lon + max_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles=None)

    tiles_list = {
        "ESRI全球影像": {"tiles": "Esri.WorldImagery", "name": "ESRI全球影像", "control": True, "overlay": False},
        "Carto地图": {"tiles": "CartoDB.Positron", "name": "Carto地图", "control": True, "overlay": False},
        "高德地图": {"tiles": "Gaode.Normal", "name": "高德地图", "control": True, "overlay": False}
    }
    for name, params in tiles_list.items():
        folium.TileLayer(tiles=params["tiles"], name=params["name"], control=params["control"],
                         overlay=params["overlay"]).add_to(m)

    # 鼠标位置
    mouse_position = MousePosition(position='bottomright', separator=' : ')
    mouse_position.add_to(m)

    # 使用矩形框表示长江流域范围
    folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]], color='red', fill=False,
                     popup='长江流域范围').add_to(m)

    folium.LayerControl().add_to(m)
    folium_static(m)


def sys_index():
    """
    系统指引，说明系统功能，初步显示长江流域信息
    """
    st.markdown("# 欢迎来到共饮长江水系统:sparkles:")
    st.sidebar.success("在上方选择各标签页")
    st.markdown("""
    长江，又名扬子江（英文：Yangtze River），古称江水、大江，简称江，是亚洲第一长河和世界第三长河，也是世界上完全在一国境内的最长河流，全长6300公里，干流发源于青藏高原东部唐古拉山脉各拉丹冬峰，穿越中国西南（青海、西藏、云南、四川、重庆）、中部（湖北、湖南、江西）、东部（安徽、江苏），在上海市汇入东海。长江流域覆盖中国大陆五分之一陆地面积，养育中国大陆三分之一的人口。长江经济带也是中国最大的经济带之一。  

    长江和黄河并称为中华文化的母亲河，孕育了长江文明和黄河文明。据2019年数据，长江三角洲经济区约占中国GDP的24%，人口规模达到2.27亿。长江流域生态类型多样，水生生物资源丰富，是多种濒危动物如扬子鳄和达氏鲟的栖息地。几千年来，人们利用长江取水、灌溉、排污、运输、发展工业、当作边界等。      
        """)
    st.markdown("""
        人们对长江有着特殊的情感，八十年代的纪录片 [《话说长江》](https://www.bilibili.com/video/BV1Gs411m744/?share_source=copy_web&vd_source=79d62c8b6140a7de77e848a9a9c40c45)被誉为中国纪录片之最，主题曲长江之歌也成为了一代人的长江记忆。时隔二十年， [《再说长江》](https://www.bilibili.com/video/BV1qs411S7J1/?share_source=copy_web)依然能吸引人们的注意。

        千年前我们的祖先于此取水灌溉、以河护城，如今长江作为黄金水道，承载着财富的流通与污染的净化，长江总能带给人澎湃的情感。许多人都对长江怀有特殊的情感，我也不例外。        
            """)
    st.markdown('\n')
    st.markdown('###### 长江流域范围示意')
    changjiang_map()

    st.markdown('我们不妨从长江入海口所在地——上海出发，沿途向上，看一看长江流域的城市')
    st.markdown('从生态环境（以空气质量）为例、娱乐与文化、安全三个方面对城市进行评估')


sys_index()
