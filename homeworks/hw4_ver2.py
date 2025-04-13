import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

# 载入Edge浏览器的driver并获取对应链接网页
driver = webdriver.Edge()
driver.get("https://sh.lianjia.com/ershoufang/rs吴泾/")
time.sleep(3)  # 等待页面加载

# 创建一个空的DataFrame用于存储数据，然后遍历所有页面，并将每个页面的房屋信息都存储到此dataframe中
data = pd.DataFrame(columns=['位置', '房屋信息', '价格信息'])
flag = True
page = 1
while flag:
    print(f"正在处理第 {page} 页...")
    if page != 1:  # 先处理第一页，再翻页
        try:  # 如果页面上能检索到“下一页”链接，则说明还没有翻遍所有页面，点击按钮，如果不能，则说明当前已经是最后一页
            next_page_button = driver.find_element(By.LINK_TEXT, '下一页')
            # selenium的click()方法使用会出现问题，因此使用JS脚本实现
            driver.execute_script('arguments[0].click()', next_page_button)
            time.sleep(2)  # 等待页面加载
        except NoSuchElementException:  # 提示用户当前已经是最后一页，输出检索完毕的信息，并将flag的值修改为False结束while循环
            print(f"第{page}页不存在！检索完毕，共{page - 1}页信息\n")
            flag = False

    # 获取当前页面的二手房信息
    houses = driver.find_elements(By.XPATH, "/html/body/div[4]/div[1]/ul/li")
    for house in houses:
        location = house.find_element(By.CLASS_NAME, "positionInfo").text
        house_info = house.find_element(By.CLASS_NAME, "houseInfo").text
        price_info = house.find_element(By.CLASS_NAME, "priceInfo").text
        new_house = pd.DataFrame({'位置': [location], '房屋信息': [house_info], '价格信息': [price_info]})
        data = pd.concat([data, new_house])  # pandas中append()为私有方法，因此通过拼接的方法实现追加
    page = page + 1  # 当前页面操作完毕，page+1进入下一轮循环

# 将数据保存到Excel文件
data.to_excel("闵行区吴泾镇二手房信息.xlsx", index=False)
print("二手房信息数据已保存到 闵行区吴泾镇二手房信息.xlsx")
# 关闭浏览器
driver.close()
