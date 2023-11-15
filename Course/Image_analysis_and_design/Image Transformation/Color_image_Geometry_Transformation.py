from math import fabs
from PIL import Image
import numpy as np

""""
对图像进行一系列 几何变换
"""

"""图像 平移操作
tx 表示水平移动，为正数 向右移动，为负数向左移动
ty 表示垂直移动，为正数 向下移动，为负数向上移动
type 表示平移类型，0 表示剪切平移，1表示循环平移
"""
def translation(image,tx,ty,type):

    w,h,c = image.shape
    imageT = np.zeros(image.shape,np.uint8)

    # 平移变换
    for i in range(c):
        for x in range(w):
            for y in range(h):
                if type==0: # 剪切
                    if((x+tx >= 0 and x+tx < w) and (y+ty>=0 and y+ty<h)):
                        imageT[x+tx,y+ty,i] = image[x,y,i]
                else: # 循环
                    imageT[(x + tx+w)%w,(y + ty+h)%h,i] = image[x,y,i]
    return imageT

""""图像 旋转操作
angele 表示旋转角度(角度制，如：10°)
type 表示旋转类型，0 表示剪切，1 表示填充
"""
def rotate(image,angle,type):

    w,h,c = image.shape
    M = np.zeros((2,3),dtype=np.float32) # 旋转矩阵
    cosA= np.cos(angle/180*np.pi)
    sinA=np.sin(angle/180*np.pi)
    M[0,0],M[0,1],M[1,0],M[1,1] = cosA,-sinA,sinA,cosA
    M[0,2],M[1,2] = (1-cosA)*w/2+sinA*h/2,(1-cosA)*h/2-sinA*w/2
    imageR = np.zeros(image.shape,np.uint8)
    new_W, new_H = int(w * fabs(cosA) + h * fabs(sinA)), int(w * fabs(sinA) + h * fabs(cosA)) # 填充旋转后的大小
    if type==1:
        M[0, 2] += (new_W - w) / 2
        M[1, 2] += (new_H - h) / 2
        imageR = np.zeros((new_W, new_H, c), np.uint8)

    for i in range(c):
        for x in range(w):
            for y in range(h):
                if type==0: #  剪切
                    new_pos = np.dot(M, np.array([[x], [y], [1]]))
                    newX, newY = round(new_pos[0, 0]), round(new_pos[1, 0])
                    if((newX>=0 and newX<w)and(newY>=0 and newY<h)):
                        imageR[newX,newY,i] = image[x,y,i]
                else: # 填充
                    new_pos = np.dot(M, np.array([[x], [y], [1]]))
                    newX, newY = round(new_pos[0, 0]), round(new_pos[1, 0])
                    imageR[newX,newY,i] = image[x,y,i]
    return imageR


""""对图像进行插值
type 表示插值类型,0 表示邻近插值法 , 1 表示均值插值
"""
def Interpolation(image,type):

    w,h,c = image.shape

    for i in range(c):
        for x in range(1,w-1):
            for y in range(1,h-1):
                if type==0: # 邻近插值法
                    if (image[x, y, i] == 0 and image[x - 1, y, i] > 0 and image[x, y - 1, i] > 0 and image[x, y + 1, i] > 0 and image[x + 1, y, i] > 0):
                        image[x,y,i] = image[x-1,y,i]
                if type==1: # 均值插值法
                    if (image[x, y, i] == 0 and image[x - 1, y, i] > 0 and image[x, y - 1, i] > 0 and image[
                        x, y + 1, i] > 0 and image[x + 1, y, i] > 0):
                        image[x,y,i] = round((image[x-1,y,i]+image[x,y-1,i]+image[x+1,y,i]+image[x,y+1,i])/4)

    return image

if __name__ == '__main__':

    path = "../../data/HW/Image Transformation/Geometry_Transformation"
    image_path= "../../data/HW/Image Transformation/Histogram_Average/test5.jpg"
    image_pil = Image.open(image_path) # 读取图片
    image_np = np.array(image_pil) # 转换为 array 格式

    # 图像 平移操作
    tx1,tx2 = 200,-200
    ty1,ty2 = 200,-200

    imageT_np1=translation(image_np,tx1,ty1,0)
    imageT_np2=translation(image_np,tx2,ty2,0)
    imageT_pil1 = Image.fromarray(imageT_np1)
    imageT_pil2 = Image.fromarray(imageT_np2)
    imageT_pil1.save(path+"/T(200,200).jpg")
    imageT_pil2.save(path+"/T(-200,-200).jpg")

    imageT_np3 = translation(image_np, tx1, ty1,1)
    imageT_np4 = translation(image_np, tx2, ty2,1)
    imageT_pil3 = Image.fromarray(imageT_np3)
    imageT_pil4 = Image.fromarray(imageT_np4)
    imageT_pil3.save(path+"/TC(200,200).jpg")
    imageT_pil4.save(path+"/TC(-200,-200).jpg")

    # 图像 旋转操作
    angle1 = 30
    angle2 = -30
    imageR_np1 = rotate(image_np, angle1, 0)  # 剪切旋转
    imageR_pil1 = Image.fromarray(imageR_np1)
    imageR_pil1.save(path + "/CR+30°.jpg")
    imageR_np1 = rotate(image_np,angle1,1) # 填充旋转
    imageR_pil1 = Image.fromarray(imageR_np1)
    imageR_pil1.save(path+"/R+30°.jpg")
    imageR_np1 = Interpolation(imageR_np1,0) # 邻近插值
    imageR_pil1 = Image.fromarray(imageR_np1)
    imageR_pil1.save(path+"/R+30°_near.jpg")
    imageR_np1 = Interpolation(imageR_np1, 1)  # 均值插值
    imageR_pil1 = Image.fromarray(imageR_np1)
    imageR_pil1.save(path + "/R+30°_aver.jpg")

    imageR_np2 = rotate(image_np, angle2, 0)  # 剪切旋转
    imageR_pil2 = Image.fromarray(imageR_np2)
    imageR_pil2.save(path + "/CR-30°.jpg")
    imageR_np2 = rotate(image_np, angle2, 1)  # 填充旋转
    imageR_pil2 = Image.fromarray(imageR_np2)
    imageR_pil2.save(path+"/R-30°.jpg")
    imageR_np2 = Interpolation(imageR_np2, 0)  # 邻近插值
    imageR_pil2 = Image.fromarray(imageR_np2)
    imageR_pil2.save(path+"/R-30°_near.jpg")
    imageR_np2 = Interpolation(imageR_np2, 1)  # 均值插值
    imageR_pil2 = Image.fromarray(imageR_np2)
    imageR_pil2.save(path + "/R-30°_aver.jpg")



