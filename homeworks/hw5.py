from pyproj import transform,Proj
import streamlit as st

st.write('10214507042 阎格:sparkles:')

# 计算东偏和北偏值
meridian1 = 121+27/60+52/3600
sh_lat = 31+14/60+7/3600  # 上海2000的坐标原点纬度
sh_lon = 121+28/60+1/3600  # 上海2000的坐标原点经度
# 先构建以东经121°27′52″为中央子午线的高斯-克吕格投影坐标系统
ori_guass = Proj(proj='tmerc', lat_0=0, lon_0=meridian1, k_0=1, x_0=0, y_0=0, ellps='WGS84',units='m')
x, y = ori_guass(sh_lon, sh_lat)
offset_e,offset_n=-x,-y

# 定义不同椭球体下的上海2000坐标系统
sh2000_cgcs2000=Proj(proj='tmerc', lat_0=0, lon_0=meridian1, k_0=1, x_0=offset_e, y_0=offset_n, ellps='WGS84',units='m')
sh2000_iau76=Proj(proj='tmerc', lat_0=0, lon_0=meridian1, k_0=1, x_0=offset_e, y_0=offset_n, ellps='IAU76',units='m')

with st.form(key="my_form"):
    st.markdown("#### 计算上海2000坐标系的东偏与北偏")
    calculate_button = st.form_submit_button(label="计算")
    if calculate_button:
        st.write(f"({x},{y})")

    st.markdown("#### CGCS2000转为上海2000投影坐标")
    choice = st.radio(label='选择坐标参照系统',options=['上海2000坐标系统(WGS84地球椭球体)', '上海2000坐标系统(IAU76地球椭球体)'])
    longtitude = st.number_input(label='输入经度（120-122）', min_value=120.000, max_value=122.000, value=121.456,format='%.3f',step=0.001,help="请输入经度")
    latitude = st.number_input(label='输入纬度（30-32）', min_value=30.000, max_value=32.000, value=31.038,format='%.3f',step=0.001,help='请输入纬度')
    sure_button = st.form_submit_button(label="提交")
    if sure_button:
        if choice=='上海2000坐标系统(WGS84地球椭球体)':
            result=transform(Proj(init='epsg:4326'),sh2000_cgcs2000,longtitude,latitude)
        else:
            result=transform(Proj(init='epsg:4326'),sh2000_iau76,longtitude,latitude)
        st.write(f"({result[0]:.2f},{result[1]:.2f})")
