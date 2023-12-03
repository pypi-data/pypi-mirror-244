import ctypes.wintypes

import cv2
import numpy as np


def extract_color_regions(image, color_ranges):
    if not color_ranges:
        return image

    # 将图像转换为RGB格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    extracted_pixels = np.zeros_like(image)  # 初始化提取像素的数组

    for target_color, color_range in color_ranges.items():
        # 将目标颜色转换为RGB数组
        target_color_rgb = tuple(int(target_color[i:i + 2], 16) for i in (0, 2, 4))

        # 将颜色范围转换为RGB范围
        color_range_values = tuple(int(color_range[i:i + 2], 16) for i in (0, 2, 4))
        color_range_min = np.subtract(target_color_rgb, color_range_values)
        color_range_max = np.add(target_color_rgb, color_range_values)

        # 创建一个布尔掩码，标识与指定颜色及其偏色范围匹配的像素
        mask = np.all((image >= color_range_min) & (image <= color_range_max), axis=2)

        # 使用布尔掩码提取匹配的像素，并替换为白色
        extracted_pixels[mask] = [255, 255, 255]

    # 将提取的像素转换为OpenCV格式
    extracted_image = cv2.cvtColor(extracted_pixels, cv2.COLOR_RGB2BGR)

    return extracted_image


def capture_window(hwnd, x1: int, y1: int, x2: int, y2: int):
    # 定义Windows API函数和类型
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    SRCCOPY = 0x00CC0020

    # 获取窗口DC
    hdc_window = user32.GetDC(hwnd)

    # 创建兼容的DC
    hdc_compatible = gdi32.CreateCompatibleDC(hdc_window)

    # 计算截图区域的宽度和高度
    width = x2 - x1
    height = y2 - y1

    # print('x y', x1, y1, x2, y2)
    # print(width, 'width')
    # print(height, 'height')

    # 创建兼容的位图
    hbitmap = gdi32.CreateCompatibleBitmap(hdc_window, width, height)

    # 选择位图到兼容的DC中
    gdi32.SelectObject(hdc_compatible, hbitmap)

    # 拷贝窗口DC到兼容的DC中，只截取指定区域
    gdi32.BitBlt(hdc_compatible, 0, 0, width, height, hdc_window, x1, y1, SRCCOPY)

    # 获取位图数据
    buffer_size = width * height * 4
    buffer = ctypes.create_string_buffer(buffer_size)
    gdi32.GetBitmapBits(hbitmap, buffer_size, buffer)

    # 将位图数据转换为OpenCV图像对象
    image_array = np.frombuffer(buffer, dtype=np.uint8)
    image = cv2.cvtColor(image_array.reshape((height, width, 4)), cv2.COLOR_BGRA2BGR)

    # 释放资源
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc_compatible)
    user32.ReleaseDC(hwnd, hdc_window)

    return image


# def matchTemplate(image, template):
# 
#     # 选择匹配方法
#     method = cv2.TM_CCOEFF_NORMED
# 
#     # 使用模板匹配方法
#     result = cv2.matchTemplate(image, template, method)
#     # 定位匹配结果的最大和最小值以及它们的位置
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     # print(max_val)
# 
#     # 如果使用的是平方差匹配方法（cv2.TM_SQDIFF或cv2.TM_SQDIFF_NORMED），则选择最小值
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         match_loc = min_loc
#     else:
#         match_loc = max_loc
# 
#     # 获取模板的宽度和高度
#     template_w, template_h = template.shape[1], template.shape[0]
# 
#     # copy_image = np.copy(image)
#     # # 在原始图像上绘制匹配结果的矩形框
#     # cv2.rectangle(copy_image, match_loc, (match_loc[0] + template_w, match_loc[1] + template_h), (0, 255, 0), 2)
#     #
#     # # 在矩形框的左上角显示坐标
#     # text = f'({match_loc[0]}, {match_loc[1]})-{max_val}'
#     # font = cv2.FONT_HERSHEY_SIMPLEX
#     # font_scale = 0.5
#     # font_color = (0, 255, 0)  # 文本颜色设置为绿色
#     # font_thickness = 1
#     # text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
#     # text_x = match_loc[0]
#     # text_y = match_loc[1] - 10  # 微调文本位置，使其显示在矩形框上方
#     # cv2.putText(copy_image, text, (text_x, text_y), font, font_scale, font_color, font_thickness)
#     #
#     # cv2.imshow('111', copy_image)
#     # cv2.imshow('222', template)
#     # cv2.waitKey(0)
# 
#     return match_loc[0] + template_w / 2, match_loc[1] # + template_h / 2


def matchTemplate(image, template, threshold=0.1):
    # 选择匹配方法
    method = cv2.TM_CCOEFF_NORMED

    # 使用模板匹配方法
    result = cv2.matchTemplate(image, template, method)
    # 定位匹配结果的最大和最小值以及它们的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val < threshold:
        return []
    # 如果使用的是平方差匹配方法（cv2.TM_SQDIFF或cv2.TM_SQDIFF_NORMED），则选择最小值
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        match_loc = min_loc
    else:
        match_loc = max_loc

    # 获取模板的宽度和高度
    template_w, template_h = template.shape[1], template.shape[0]

    copy_image = np.copy(image)
    # 在原始图像上绘制匹配结果的矩形框
    cv2.rectangle(copy_image, match_loc, (match_loc[0] + template_w, match_loc[1] + template_h), (0, 255, 0), 2)

    # 在矩形框的左上角显示坐标
    # text = f'({match_loc[0]}, {match_loc[1]})-{max_val}'
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # font_scale = 0.5
    # font_color = (0, 255, 0)  # 文本颜色设置为绿色
    # font_thickness = 1
    # text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    # text_x = match_loc[0]
    # text_y = match_loc[1] - 10  # 微调文本位置，使其显示在矩形框上方
    # cv2.putText(copy_image, text, (text_x, text_y), font, font_scale, font_color, font_thickness)
    # 
    # cv2.imshow('111', copy_image)
    # # cv2.imshow('222', template)
    # cv2.waitKey(50)

    return [int(match_loc[0] + template_w / 2), int(match_loc[1] + template_h / 2)]


if __name__ == '__main__':
    img = capture_window(725022, 0, 0, 1280, 768)
    cv2.imshow('1', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
