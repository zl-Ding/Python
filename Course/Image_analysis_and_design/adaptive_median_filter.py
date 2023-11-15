import cv2
from skimage import util
import skimage
from PIL import Image
import numpy as np


def image_save(image,path):
    image.save(path)

""" 自适应中值滤波
image 表示 待去噪图像
max_depth 表示 最大滤波窗口
"""
def adaptive_median_filter(image,max_size):

    w,h,c = image.shape
    res = np.zeros((w,h,c),dtype=np.uint8)
    padding = max_size // 2 # 填充图像 边界大小

    for i in range(c):
        image_channels = np.pad(image[:, :, i],((padding,padding),(padding,padding)),mode='edge') # 获取 单通道的图像，并对该通道进行填充
        for j in range(w):
            for k in range(h):
                res[j,k,i] = adMedFil_stepA(image_channels,max_size,j+padding,k+padding) # 自适应中值滤波取值函数
    return res

"""自适应中值滤波 阶段A
"""
def adMedFil_stepA(image,max_size,j,k):
    size = 3
    padding = size//2 # 滤波窗口边界

    while(size <= max_size): # 寻找到一个合适窗口
        conv_window = image[j-padding:j+padding+1,k-padding:k+padding+1]
        med = np.median(conv_window)
        min = np.min(conv_window)
        max = np.max(conv_window)
        if(min<med and med <max): return adMedFil_stepB(conv_window,size,max,min,med) # 找到后执行B阶段
        padding +=1
        size += 2
    return np.round(med).astype(np.uint8)

"""自适应中值滤波 阶段B
"""
def adMedFil_stepB(conv_window,size,max,min,med):

    x = conv_window[size//2,size//2]
    # 输出 原值或中值
    if(x < max and x > min): return x
    return np.round(med).astype(np.uint8)


if __name__ == '__main__':

    path = "../data/HW/Adaptive_median_filter/house/0.8/"
    image = Image.open(path+"house1024.jpg")
    
    svp = 0.5 # 椒盐噪声出现的概率
    image_noise = np.rint(skimage.util.random_noise(np.array(image), mode='s&p', salt_vs_pepper=0.8, clip=True) * 255).astype(np.uint8)
    image_save(Image.fromarray(image_noise),path+"svp0.8.jpg")

    # 中值滤波，窗口大小为3，5，7
    image_median_3 = cv2.medianBlur(image_noise,3)
    image_median_5 = cv2.medianBlur(image_noise,3)
    image_median_7 = cv2.medianBlur(image_noise,3)

    image_save(Image.fromarray(image_median_3),path+"med_3.jpg")
    image_save(Image.fromarray(image_median_5),path+"med_5.jpg")
    image_save(Image.fromarray(image_median_7),path+"med_7.jpg")

    # 自适应中值滤波
    image_adMedFilter_7 = adaptive_median_filter(image_noise,7)
    image_adMedFilter_9 = adaptive_median_filter(image_noise,9)
    image_adMedFilter_11 = adaptive_median_filter(image_noise,11)

    image_save(Image.fromarray(image_adMedFilter_7),path+"ad_med_filter_7.jpg")
    image_save(Image.fromarray(image_adMedFilter_9),path+"ad_med_filter_9.jpg")
    image_save(Image.fromarray(image_adMedFilter_11),path+"ad_med_filter_11.jpg")


