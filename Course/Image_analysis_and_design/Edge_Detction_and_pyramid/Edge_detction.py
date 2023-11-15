import cv2
from PIL import Image
import numpy as np

def image_save(image,path):
    image.save(path)

"""根据指定算子的边缘检测
image 表示传入的图像，为array格式
kernelx 表示x轴检测核
kernely 表示y轴检测核
path 表示图片保存路径
str 表示算子类别
"""
def My_Detection(image,kernelx,kernely,path,str):

    x = cv2.filter2D(image,cv2.CV_16S ,kernelx)
    y = cv2.filter2D(image,cv2.CV_16S ,kernely)

    absX = cv2.convertScaleAbs(x)  # 转为uint8
    absY = cv2.convertScaleAbs(y)

    img_x = Image.fromarray(absX)
    img_y = Image.fromarray(absY)

    image_save(img_x, path + str+"_x.jpg")
    image_save(img_y, path +str +"_y.jpg")

    # res = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    res = np.clip(absX+absY, 0, 255)

    image_save(Image.fromarray(res), path +str+ ".jpg")

    return res

"""基于Sobel算子的边缘检测
image 表示传入的图像，为array格式
path 表示图片保存路径
"""
def Sobel_Detection(image,path):

    x = cv2.Sobel(image, cv2.CV_16S, 1,0)
    y = cv2.Sobel(image, cv2.CV_16S, 0,1)

    absX = cv2.convertScaleAbs(x) # 转为uint8
    absY = cv2.convertScaleAbs(y)

    img_x = Image.fromarray(absX)
    img_y = Image.fromarray(absY)

    image_save(img_x,path+"Sobel_x.jpg")
    image_save(img_y,path+"Sobel_y.jpg")

    # res = cv2.addWeighted(absX, 0.5, absY, 0.5,0)
    res = np.clip(absX+absY, 0, 255)

    image_save(Image.fromarray(res),path+"Sobel.jpg")

    return res


if __name__ == '__main__':

    path = "../../data/HW/Edge_Detection_and_pyramid/Edge_detection/house/"

    image= Image.open(path+"house.jpg") # 读取图片
    image_np = np.array(image) # 转换为 array 格式

    image_gry_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    image_save(Image.fromarray(image_gry_np), path+"house_gray.jpg") # 保存图像

    # Roberts 算子
    kernelx = np.array([[-1,0],[0,1]],dtype=int)
    kernely = np.array([[0,-1],[1,0]],dtype=int)
    image_Roberts_np = My_Detection(image_gry_np,kernelx,kernely,path,"Roberts")

    # Prewitt 算子
    kernelx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=int)
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=int)
    image_Prewitt_np = My_Detection(image_gry_np,kernelx,kernely,path,"Prewitt")

    # Sobel 算子
    image_Sobel_np = Sobel_Detection(image_gry_np,path)

    # Lablacian 算子
    image_lap_np = cv2.convertScaleAbs(cv2.Laplacian(image_gry_np,cv2.CV_16S,ksize=3))
    image_save(Image.fromarray(image_lap_np), path+"lap.jpg")

    # Canny 算子
    image_canny_np = cv2.Canny(image_gry_np, 50, 150)
    image_save(Image.fromarray(image_canny_np), path+"canny.jpg")







