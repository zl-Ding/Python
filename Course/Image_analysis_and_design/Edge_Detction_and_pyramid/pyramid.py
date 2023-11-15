from PIL import Image
import numpy as np
import cv2
import pywt

def image_save(image,path):
    image.save(path)

"""构建gaussian金字塔
image 表示传入图像
high 表示金字塔高度
返回一个gaussian金字塔
"""
def gaussian_pyramid(image,high,path):

    pyramid = [image,]
    for i in range(high):
        pyramid.append(cv2.pyrDown(pyramid[i]))
        image_save(Image.fromarray(pyramid[i+1]),path+f"gauss_{i+1}.jpg")

    return pyramid

"""构建laplacian金字塔
gauss_pyramid 表示传入的高斯金字塔
high 表示金字塔高度
返回一个laplacian金字塔
"""
def laplacian_pyramid(gauss_pyramid,path):

    high = len(gauss_pyramid)
    pyramid = [gauss_pyramid[high-1],]
    for i in range(high-1):
        pyramid.append(gauss_pyramid[high-i-2]-cv2.pyrUp(gauss_pyramid[high-i-1]))
        image_save(Image.fromarray(pyramid[i+1]),path+f"lap_{i+1}.jpg")

    return pyramid

"""构建wavelet金字塔
image 表示传入图像
level 表示 wavelet 深度 
返回一个小波金字塔
"""
def wavelet_pyramid(image,level,path):

    pyramid = [[image],]

    for i in range(level):
        ll,(lh,hl,hh) = pywt.dwt2(pyramid[i][0],'haar')
        pyramid.append([ll,lh,hl,hh])
        image_save(Image.fromarray(pyramid[i+1][0]).convert('RGB'),path+f"wavelet_{i+1}_ll.jpg")
        image_save(Image.fromarray(pyramid[i+1][1]).convert('RGB'),path+f"wavelet_{i+1}_lh.jpg")
        image_save(Image.fromarray(pyramid[i+1][2]).convert('RGB'),path+f"wavelet_{i+1}_hl.jpg")
        image_save(Image.fromarray(pyramid[i+1][3]).convert('RGB'),path+f"wavelet_{i+1}_hh.jpg")

    return pyramid

if __name__ == "__main__":

    path = "../../data/HW/Edge_Detection_and_pyramid/Pyramid/house/"

    image = Image.open(path+"house.jpg")
    image_np = np.array(image)
    image_np = image_np[0:1024,300:1324] # 对照片进行裁剪
    image_save(Image.fromarray(image_np),path+"house1024.jpg")

    image_gry_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    image_save(Image.fromarray(image_gry_np), path + "house_gray.jpg")  # 保存图像

    high = 6

    # 构建gaussian金字塔
    gauss_pyramid = gaussian_pyramid(image_np,high,path)

    # 构建laplacian 金字塔
    lap_pyramid = laplacian_pyramid(gauss_pyramid,path)

    level = 3

    # 构建 wavelet 金字塔
    wavelet_pyramid = wavelet_pyramid(image_gry_np,level,path)