import math # 导入math函数以计算
r=20037508.34 # 定义常数值r
def main():
    """
    主屏幕，展示可选操作并提示用户输入数字选择
    """
    print("----------进入操作----------")
    print("1.WGS84经纬度坐标转Web墨卡托投影坐标")
    print("2.Web墨卡托投影坐标转WGS84经纬度坐标")
    print("3.退出操作")
    return int(input("请输入您想要进行的操作(1-3):"))

def WGS_to_Web(long,lati):
    x=long*r/180
    y=math.log(math.tan(math.pi/4+lati*math.pi/360))*r/math.pi
    return x,y

def Web_to_WGS(x,y):
    long=x/r*180
    rati=math.atan(math.pow(math.e,y*math.pi/r))*360/math.pi-90
    return long,rati
# 主程序，定义flag=True，利用while进行无线循环，便于用户多次操作，通过flag=False和break语句退出死循环
flag=True
while flag:
    choi=main()
    if choi==1:
        long,rati=map(int,input("请输入经度和纬度坐标（之间用逗号分隔）：").split(','))
        x,y=WGS_to_Web(long,rati)
        print(f"x:{x}\ty:{y}")
    elif choi==2:
        x,y=map(int,(input("请输入x、y投影坐标(之间用逗号分隔):")).split(','))
        long,rati=Web_to_WGS(x,y)
        print("经度:%.2f\t纬度:%.2f"% (long,rati))
    else:
        flag=False
        break
