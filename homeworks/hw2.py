import streamlit as st
import pandas as pd

st.write('10214507042 阎格:sparkles:')
st.markdown("# 长三角PM2.5监测数据")  # 标题

# 读取数据存储到frame中
url_data = "https://EcnuGISChaser.github.io/gis_development/data/csj_pm25.csv"
frame = pd.read_csv(url_data, encoding="utf8")

# 使用可收展的容器显示原始数据
with st.expander("##### 显示原始数据"):
    st.dataframe(frame)  # 以dataframe形式显示原始数据

# 使用表单完成基于属性表达式查询记录
months = frame.columns[4:].tolist()
compare=['>','<']

with st.form(key="my_form"):
    st.markdown("#### 基于属性表达式查询记录")
    selected_month=st.selectbox(label='选择一个查询月份', options=months, index=0, help="请选择一个月份")
    com=st.selectbox(label='选择一个关系',options=compare,index=0,help="请选择判断关系")
    value = st.text_input("输入一个值",help="请输入值")
    submit_button=st.form_submit_button(label="提交")

    if submit_button:
        value=(float(value))  # 转换类型以便后续比较
        if com=="<":
            exp= frame[selected_month] < value
            new_frame= frame[exp]
        else:
            exp = frame[selected_month] > value
            new_frame = frame[exp]
        count = new_frame.shape[0]  # 计数
        st.write("##### 共有"+str(count)+"条数据")
        st.dataframe(new_frame)  # 以dataframe的形式显示子集数据

        # 在地图上显示子集对应的监测点
        st.markdown("##### 地图上各监测点位置")
        new_frame["longitude"]=new_frame["经度"]
        new_frame["latitude"]=new_frame["纬度"]
        st.map(new_frame)
