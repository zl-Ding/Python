import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

"""
读入彩色图片，分别在RGB三个通道进行直方图均值化
"""

MAX_SIZE = 256

# 显示图像的直方图
def plot(image_y, image_Hy, str):

    x = [i for i in range(MAX_SIZE)]

    fig, ax1 = plt.subplots()  # 生成一个 Figure 画布 和一个Axes 坐标系
    ax1.plot(x, image_Hy, color="lawngreen", label=u'累积个数')  # 折线图
    ax1.set_ylim([0,image_Hy[MAX_SIZE-1]*1.2])   # 添加纵轴的刻度
    ax1.legend(loc=2)

    ax2 = ax1.twinx()  # 建立第二个坐标系
    plt.bar(x, image_y, color="violet", label=u'像素个数')
    ax2.set_ylim([0, image_Hy[MAX_SIZE-1]/10])  # 添加纵轴的刻度
    # ax2.set_ylabel("像素个数")
    ax2.legend(loc=1)

    plt.title(str + "直方图")  # 添加标题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.show()  # 显示图像

# 计算单通道直方图
def calcHist(image_np,str):

    cell_num = np.size(image_np)  # 计算图像像素个数
    w,h = image_np.shape # 获取图像的长宽

    image_y = [np.sum(image_np == i) for i in range(MAX_SIZE)]  # 原图直方图
    image_Hy = [sum(image_y[:i]) for i in range(MAX_SIZE)]  # 计算前 i 项和
    plot(image_y, image_Hy,str+" 原图")  # 显示直方图

    # 均值化
    hList = [round(image_Hy[i]/cell_num*(MAX_SIZE-1))
                for i in range(MAX_SIZE)]    # 映射表

    imageH_np= np.zeros((w,h),np.uint8)
    # for x in range(w):  # 替换
    #     for y in range(h):
    #         imageH_np[x,y] = hList[image_np[x,y]]
    for i in range(MAX_SIZE):   # 替换
        imageH_np[image_np==i] = hList[i]

    imageH_y = [np.sum(imageH_np == i) for i in range(MAX_SIZE)]  # 均值化后的直方图
    imageH_Hy = [sum(imageH_y[:i]) for i in range(MAX_SIZE)]  # 计算前 i 项和
    plot(imageH_y, imageH_Hy, str + "均值化后")   # 显示直方图

    return imageH_np

# 分别保存图像RGB三个通道的图像
def image_save(image,path,str):
    
    zeros = np.zeros(image[0].shape,dtype="uint8") # 创建 全0 通道
    # B 通道图像
    imageB_np = np.array([zeros, zeros,image[0]]).swapaxes(0, 2)  # 合并每一个通道
    imageB = Image.fromarray(imageB_np)  # 转换为 PIL格式
    imageB.save(f"{path}/{str}_B.jpg")

    # G 通道图像
    imageG_np = np.array([zeros,image[1] ,zeros]).swapaxes(0, 2)  # 合并每一个通道
    imageG = Image.fromarray(imageG_np)  # 转换为 PIL格式
    imageG.save(f"{path}/{str}_G.jpg")

    # R 通道图像
    imageR_np = np.array([image[2],zeros, zeros]).swapaxes(0, 2)  # 合并每一个通道
    imageR = Image.fromarray(imageR_np)  # 转换为 PIL格式
    imageR.save(f"{path}/{str}_R.jpg")
    
    

if __name__ == '__main__':

    path = "../../data/HW/Image Transformation/Histogram_Average"
    image_path = path+"/test5.jpg"
    image_pil = Image.open(image_path)  # 读取图片
    image_np = np.array(image_pil)  # 转换为array格式
    image_np = image_np.swapaxes(0,2) # 转换维度，将彩蛇通道转到低维

    image_gray = image_pil.convert('L') # 转为灰度图
    image_gray.save(path+"/test5_gray.jpg")
    image_Gnp = np.array(image_gray) # 转换为array格式

    (r,g,b) = image_np[0,:,:],image_np[1,:,:],image_np[2,:,:]  # 分解彩色图片RGB通道
    image_save([b,g,r],path,"test5")

    gH=calcHist(image_Gnp,"灰度图")
    imageH_gray = Image.fromarray(gH)
    imageH_gray.save(path+"/test5_GrayH.jpg")

    bH=calcHist(b,"B 通道")# 处理 B 通道
    gH=calcHist(g,"G 通道")# 处理 G 通道
    rH=calcHist(r,"R 通道")# 处理 R 通道
    image_save([bH,gH,rH],path,"test5H")

    imageH_np=np.array([rH,gH,bH]).swapaxes(0,2) # 合并每一个通道
    imageH = Image.fromarray(imageH_np) #转换为 PIL格式
    imageH.save(path+"/test5H.jpg") # 保存图片


