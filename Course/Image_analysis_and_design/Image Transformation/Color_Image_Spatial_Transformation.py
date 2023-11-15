
"""
对图像进行 空间变换
"""
from PIL import Image
import numpy as np
from skimage import util
import skimage

MAX_SIZE = 256

"""
给图像添加噪声
mode 表示 添加的噪声种类，实现了"gaussion"--高斯噪声，"s&p"--椒盐噪声
mean 表示 均值
sigma 表示离散程度 ，sigma = 标准差
svp 表示椒盐噪声出现的概率
"""
def addNoise(image, mode, mean=0, sigma=10, svp=0.5):

    w, h, c = image.shape
    image_noise = image
    sigma = sigma

    if mode == "gaussian":  # 高斯噪声
        # image_noise =np.rint(skimage.util.random_noise(image,mode=mode,mean=mean,var=sigma*sigma,clip=True)*(MAX_SIZE-1)).astype(np.uint8)
        gauss = np.random.normal(mean, sigma, (w, h, c)).astype(np.uint8)   # 生成服从 mean，sigma 分布的高斯噪声
        image_noise = np.clip(image+gauss,0,MAX_SIZE-1).astype(np.uint8)# 设置添加噪声后的 像素点取值范围

    elif mode == "s&p":  # 添加椒盐噪声
        # image_noise  = np.rint(skimage.util.random_noise(image,mode=mode,salt_vs_pepper=svp,clip=True)*(MAX_SIZE-1)).astype(np.uint8)
        mask = np.random.uniform(0, 1, (w, h))
        for i in range(c):
            image_noise[:, :, i][mask < svp] = MAX_SIZE - 1  # 添加salt
            image_noise[:, :, i][mask < svp / 2] = 0  # 添加 papper

    return image_noise


""" 图像 滤波器
size 表示滤波的窗口范围
mode 表示滤波 模型
sigma 表示高斯滤波的标准差
laplas 用于拉普拉斯滤波，其拉普拉斯卷积核 = sigma的高斯核 - laplas的高斯核
"""
def filter(image, size, mode, sigma=10, laplas=30):

    w, h, c = image.shape
    image_filter = np.zeros((w,h,c),np.uint8)
    padding = size // 2  # 裁剪 四周大小

    if mode == "max":  # 最大滤波
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    con_window = image[x - padding:x + padding+1,
                                       y - padding:y + padding+1, i]  # 滤波窗口
                    image_filter[x, y, i] = np.max(con_window)
    elif mode == "min":    # 最小滤波
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    con_window = image[x - padding:x + padding+1,
                                       y - padding:y + padding+1, i]  # 滤波窗口
                    image_filter[x, y, i] = np.min(con_window)
    elif mode == "mean":    # 均值滤波
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    con_window = image[x - padding:x + padding+1,
                                       y - padding:y + padding+1, i]  # 滤波窗口
                    image_filter[x, y, i] = np.round(np.mean(con_window))
    elif mode == "median":     # 中值滤波
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    con_window = image[x - padding:x + padding+1,
                                       y - padding:y + padding+1, i]  # 滤波窗口
                    image_filter[x, y, i] = np.median(con_window)
    elif mode == "gaussian":  # 高斯滤波
        gaussian_window = np.fromfunction(
            lambda x, y: ((1 / (2 * np.pi * sigma**2) * np.exp(-(((x - padding)**2) + (y - padding)**2) / 2 * sigma**2))),
            (size, size)
        )  # 高斯滤波窗口
        gaussian_window /= np.sum(gaussian_window)  # 归一化
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    image_filter[x, y, i] = np.round(np.sum(
                        gaussian_window * image[x - padding:x + padding+1, y - padding:y + padding+1, i]))
    elif mode == "gaussian":  # 拉普拉斯滤波
        gaussian_window1 = np.fromfunction(
            lambda x, y: ((1 / (2 * np.pi * sigma**2) * np.exp(-(((x - padding)**2) + (y - padding)**2) / 2 * sigma**2))),
            (size, size)
        )  # sigma 卷积核
        gaussian_window2 = np.fromfunction(
            lambda x, y: (
                (1 / (2 * np.pi * laplas ** 2) * np.exp(-(((x - padding) ** 2) + (y - padding) ** 2) / 2 * laplas ** 2))),
            (size, size)
        )  # laplas 卷积核
        laplas_window = gaussian_window1 - gaussian_window2
        laplas_window /= np.sum(laplas_window)  # 归一化
        for i in range(c):
            for x in range(padding, w - padding):
                for y in range(padding, h - padding):
                    image_filter[x, y, i] = np.round(np.sum(
                        laplas_window * image[x - padding:x + padding+1, y - padding:y + padding+1, i]))

    return image_filter


if __name__ == '__main__':

    path = "../../data/HW/Image Transformation/Spatial_Transformation/"
    image_path = path + "svp0.05.jpg"

    image_pil = Image.open(image_path)  # 读取图片
    image_np = np.array(image_pil)  # 转换为array 格式

    # image_svp = np.array(Image.open(image_path))

    # 添加高斯噪声
    sigma = 10
    image_gauss = addNoise(image_np, "gaussian", mean=0, sigma=sigma)
    image_gauss_pil = Image.fromarray(image_gauss)
    # image_gauss_pil.show()
    image_gauss_pil.save(path + f"G{sigma}.jpg")

    # 添加椒盐噪声
    svp = 0.05
    image_svp = addNoise(image_np, "s&p", svp=svp)
    image_svp_pil = Image.fromarray(image_svp)
    image_svp_pil.save(path + f"svp{svp}.jpg")
    # image_svp_pil.show()

    size = 3

    # 最大滤波
    image_svp_maxF = Image.fromarray(filter(image_svp, size, "max"))
    # image_svp_maxF.show()
    image_svp_maxF.save(path+f"size/{size}/"+"svp_max.jpg")

    # 最小滤波
    image_svp_minF = Image.fromarray(filter(image_svp, size, "min"))
    # image_svp_minF.show()
    image_svp_minF.save(path +f"size/{size}/"+ "svp_min.jpg")

    # 最大最小滤波
    image_svp_max_minF = Image.fromarray(filter(filter(image_svp, size, "max"), size, "min"))
    # image_svp_max_minF.show()
    image_svp_max_minF.save(path+f"size/{size}/" + "svp_max_min.jpg")

    # 最小最大滤波
    image_svp_min_maxF = Image.fromarray(filter(filter(image_svp, size, "min"), size, "max"))
    # image_svp_min_maxF.show()
    image_svp_min_maxF.save(path+f"size/{size}/" + "svp_min_max.jpg")

    # 中值滤波
    image_svp_medF = Image.fromarray(filter(image_svp, size, "median"))
    # image_svp_medF.show()
    image_svp_medF.save(path+f"size/{size}/" + "svp_med.jpg")
    image_gas_medF = Image.fromarray(filter(image_gauss, size, "median"))
    # image_svp_medF.show()
    image_gas_medF.save(path +f"size/{size}/"+ "gas_med.jpg")

    # 均值滤波
    image_svp_meanF = Image.fromarray(filter(image_svp, size, "mean"))
    # image_svp_meanF.show()
    image_svp_medF.save(path+f"size/{size}/" + "svp_mean.jpg")
    image_gas_meanF = Image.fromarray(filter(image_gauss, size, "mean"))
    # image_svp_medF.show()
    image_gas_meanF.save(path +f"size/{size}/"+ "gas_mean.jpg")

    # 高斯滤波
    image_svp_gasF = Image.fromarray(filter(image_svp, size, "gaussian"))
    # image_svp_gasF.show()
    image_svp_gasF.save(path+f"size/{size}/" + "svp_gas.jpg")
    image_gas_gasF = Image.fromarray(filter(image_gauss, size, "gaussian"))
    # image_svp_gasF.show()
    image_gas_gasF.save(path +f"size/{size}/"+ "gas_gas.jpg")

    # 拉普拉斯滤波
    image_svp_lapsF = Image.fromarray(filter(image_svp, size, "gaussian"))
    # image_svp_lapsF.show()
    image_svp_lapsF.save(path +f"size/{size}/"+ "svp_laps.jpg")
    image_gas_lapsF = Image.fromarray(filter(image_gauss, size, "gaussian"))
    # image_svp_lapsF.show()
    image_gas_lapsF.save(path +f"size/{size}/"+ "gas_laps.jpg")