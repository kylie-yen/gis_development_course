"""
10214507042 阎格
地图切片服务数据：高德全球影像
根据华师大闵行校区的Web墨卡托投影坐标范围生成切片的行列号序列，依据行列序号下载地图切片文件、生成world文件
"""
import requests
import math
import numpy as np

# 定义本次作业中的比例尺级别z，切片宽度/高度d，分辨率resolution
z = 15
d = 40075014 / (2 ** z)
resolution = d / 256


def tile_xy_generate(xmin, xmax, ymin, ymax, ox, oy, scale):
    """
    将已知区域Web墨卡托投影坐标范围、比例尺级别，求地图切片x y值封装为函数
    :param xmin: 区域Web墨卡托投影坐标X最小值
    :param xmax: 区域Web墨卡托投影坐标X最大值
    :param ymin: 区域Web墨卡托投影坐标Y最小值
    :param ymax: 区域Web墨卡托投影坐标X最大值
    :param ox: 原点坐标X值
    :param oy: 原点坐标Y值
    :param scale: 比例尺级别
    :return: 返回区域地图切片的x y
    """
    size = 40075014 / (2 ** scale)  # 根据比例尺级别计算切片的宽度/高度
    tile_x = []  # 存放x
    tile_y = []  # 存放y
    for i in np.arange(xmin, xmax + 1, size):  # range()方法步长不能为float类型，因此使用numpy的arange()方法
        x = math.floor((i - ox) / size)
        tile_x.append(x)
    for j in np.arange(ymin, ymax + 1, size):
        y = math.floor((abs((j - oy)) / size))
        tile_y.append(y)
    return tile_x, tile_y


# 调用tile_xy_generate()函数
mh_column, mh_row = tile_xy_generate(13518000, 13521000, 3636000, 3638100, -20037508, 20037508, z)

for col in mh_column:
    for row in mh_row:
        # 将切片图片以.png格式存储
        url = f"https://webst01.is.autonavi.com/appmaptile?style=6&x={col}&y={row}&z=15"
        response = requests.get(url)
        f1 = open(f"{z}_{row}_{col}.png", "wb")
        f1.write(response.content)
        f1.close()

        # 将world文件以.pngw格式存储
        LU_y = 20037507 - d * row
        LU_x = (d * col) - 20037507
        text = f"{resolution}\n0\n0\n-{resolution}\n{LU_x}\n{LU_y}"
        f2 = open(f"{z}_{row}_{col}.pngw", "w")
        f2.write(text)
        f2.close()
