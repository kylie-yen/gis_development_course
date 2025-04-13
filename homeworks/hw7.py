import streamlit as st
import geopandas as gpd

# 读取数据
provinces_gdf = gpd.read_file("c:/data/china/china_provinces.shp")
roads_gdf = gpd.read_file("c:/data/china/china_roads.shp")
provinces_gdf['area_km2'] = provinces_gdf['geometry'].area / 1e6  # 计算面积

st.title("查询省级行政单元的信息")
with st.form("my_form"):
    selected_province = st.selectbox("选择省级行政单元", provinces_gdf['NAME'].tolist())
    include_overlaps = st.checkbox("相邻省份包含overlaps关系")
    submitted = st.form_submit_button("查询")

if submitted:
    province = provinces_gdf[provinces_gdf['NAME'] == selected_province].iloc[0]
    area = province['area_km2']
    province_geom = province['geometry']
    # 切割出位于该省的道路
    roads_in_province = roads_gdf[roads_gdf.intersects(province_geom)]
    roads_in_province = gpd.clip(roads_gdf, province_geom)
    total_road_length_km = roads_in_province['geometry'].length.sum() / 1e3
    road_density = total_road_length_km / area

    # 查询相邻省份
    if include_overlaps:
        adjacent_provinces = provinces_gdf[
            provinces_gdf['geometry'].overlaps(province_geom) | provinces_gdf['geometry'].touches(province_geom)]
    else:
        adjacent_provinces = provinces_gdf[provinces_gdf['geometry'].touches(province_geom)]

    adjacent_provinces = adjacent_provinces[adjacent_provinces['NAME'] != selected_province]
    adjacent_province_names = adjacent_provinces['NAME'].tolist()

    # 显示结果
    st.subheader("查询结果")
    st.write(f"{selected_province}的面积: {area:.2f} 平方公里")
    st.write(f"{selected_province}的道路总长度: {total_road_length_km:.2f} 公里")
    st.write(f"{selected_province}的道路密度: {road_density:.4f} 公里/平方公里")

    st.write(f"{selected_province}相邻省份: {len(adjacent_province_names)}")
    st.markdown("$\color{red} {相邻省份名称}$")
    for name in adjacent_province_names:
        st.write(name)
