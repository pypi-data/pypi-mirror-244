import os

import cv2

import shutil

from game_tools.recognition.imageutls import extract_color_regions
from game_tools.utils.game_logging import logger

cache_path = os.path.join(os.getcwd(), 'cache/image/ocr')


def clear_cache_folder():
    try:
        cache_path = os.path.join(os.getcwd(), 'cache')
        # 删除文件夹及其内容
        shutil.rmtree(cache_path)
        print(f"Folder '{cache_path}' cleared successfully.")
    except Exception as e:
        print(f"Error clearing folder: {str(e)}")


def save_image(image, image_name):
    try:
        # 确保输出文件夹存在
        path = os.path.join(cache_path, image_name)
        output_dir = os.path.dirname(path)
        os.makedirs(output_dir, exist_ok=True)

        # 保存图像
        cv2.imwrite(path, image)
        return path
    except Exception as e:
        print(f"保存图像时出现错误: {e}")
        logger.debug(f"保存图像时出现错误: {e}")
        logger.exception(e)
        return None


class OCRDetector:

    def __init__(self, rpc_list):
        self._rpc_list = rpc_list
        clear_cache_folder()

    def paddle_ocr(self, image, name, x1, y1, x2, y2, color_ranges=None, tag='default'):
        img = self.image_color_regions(image, x1, y1, x2, y2, color_ranges)
        path = save_image(img, f'paddle-ocr-{name}.bmp')
        return self._rpc_list[0].ocr(path, tag)

    def easy_ocr(self, image, name, x1, y1, x2, y2, color_ranges=None, allowlist=None):
        img = self.image_color_regions(image, x1, y1, x2, y2, color_ranges)
        path = save_image(img, f'easy-ocr-{name}.bmp')
        return self.convert_easy_data(self._rpc_list[1].ocr(path, allowlist=allowlist))

    def image_color_regions(self, image, x1, y1, x2, y2, color_ranges=None):
        return extract_color_regions(image[int(y1):int(y2), int(x1):int(x2)], color_ranges)

    def in_string(self, result, string):
        for i in result:
            for x in i:
                if string in x[1][0]:
                    return x
        return None

    # 找出数据中字符串所在的位置
    def find_in_string(self, data, *targets):
        for target in targets:
            coordinates = self.in_string(data, target)
            if coordinates:
                return coordinates
        return None

    def string_join(self, data):
        result = ""
        for item in data:
            for ocr in item:
                result += ocr[1][0]
        return result

    def convert_easy_data(self, input_data):
        output_data = []

        for box, text, confidence in input_data:
            formatted_box = [[[[float(x), float(y)] for x, y in box]]]
            formatted_text = (text, confidence)
            output_data.append([formatted_box, formatted_text])

        return [output_data]

    def is_result_empty(self, resulet):
        if resulet is None:
            return True
        return len(resulet) == 0 or (len(resulet) == 1 and len(resulet[0]) == 0)
