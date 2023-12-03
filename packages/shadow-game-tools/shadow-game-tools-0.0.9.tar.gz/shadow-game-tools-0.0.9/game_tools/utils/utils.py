import random
import time

from game_tools.device.windows_message import MessageSender


# 返回矩形的中间坐标
def get_rectangle_center(rectangle):
    print('rectangle', rectangle)
    x1, y1, x2, y2 = rectangle
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return int(center_x), int(center_y)


# 移动镜头
def move_camera(msg: MessageSender):
    msg.send_mouse_move_to(random.randint(620, 660), random.randint(300, 340))
    msg.send_mouse_down('right')
    time.sleep(0.05)
    msg.send_mouse_move_to(random.randint(353, 500), random.randint(140, 448), 'right')
    msg.send_mouse_up('right')
    time.sleep(1)
