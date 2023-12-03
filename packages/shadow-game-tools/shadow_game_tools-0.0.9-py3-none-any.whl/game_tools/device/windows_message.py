import math
import random
import time

import win32api
import win32con
import win32gui

from game_tools.device.cBezier import bezierTrajectory

keyname_to_keycode = {
    'lbutton': 1,
    'rbutton': 2,
    'cancel': 3,
    'mbutton': 4,
    'back': 8,
    'tab': 9,
    'clear': 12,
    'enter': 13,
    'shift': 16,
    'control': 17,
    'alt': 18,
    'pause': 19,
    'capital': 20,
    'esc': 27,  # VK_ESC 替换为数字 27
    'space': 32,
    'prior': 33,
    'next': 34,
    'end': 35,
    'home': 36,
    'left': 37,
    'up': 38,
    'right': 39,
    'down': 40,
    'select': 41,
    'execute': 43,
    'snapshot': 44,
    'insert': 45,
    'delete': 46,
    'help': 47,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,  # VK_W 替换为数字 87
    'x': 88,
    'y': 89,
    'z': 90,
    'numpad0': 96,
    'numpad1': 97,
    'numpad2': 98,
    'numpad3': 99,
    'numpad4': 100,
    'numpad5': 101,
    'numpad6': 102,
    'numpad7': 103,
    'numpad8': 104,
    'numpad9': 105,
    'multiply': 106,
    'add': 107,
    'separator': 108,
    'subtract': 109,
    'decimal': 110,
    'divide': 111,
    'f1': 112,
    'f2': 113,
    'f3': 114,
    'f4': 115,
    'f5': 116,
    'f6': 117,
    'f7': 118,
    'f8': 119,
    'f9': 120,
    'f10': 121,
    'f11': 122,
    'f12': 123,
    'numlock': 144,
    'scroll': 145,
}


class MessageSender:
    def __init__(self, target_hwnd):
        self.target_hwnd = target_hwnd
        self.bezier = bezierTrajectory()
        self.last_x = random.randint(0, 1280)
        self.last_y = random.randint(0, 768)

    def send_left_click(self):
        time.sleep(0.5)
        # 模拟鼠标左键按下
        lParam = win32api.MAKELONG(self.last_x, self.last_y)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(random.uniform(0.08, 0.1))
        # 模拟鼠标左键释放
        win32gui.PostMessage(self.target_hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(random.uniform(0.1, 0.3))

    def send_right_click(self):
        time.sleep(0.5)
        # 模拟鼠标右键按下
        lParam = win32api.MAKELONG(self.last_x, self.last_y)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
        time.sleep(random.uniform(0.08, 0.1))
        # 模拟鼠标右键释放
        win32gui.PostMessage(self.target_hwnd, win32con.WM_RBUTTONUP, 0, lParam)
        time.sleep(random.uniform(0.1, 0.3))

    def send_mouse_down(self, button):
        # 模拟鼠标按键按下
        lParam = win32api.MAKELONG(self.last_x, self.last_y)
        print('鼠标按下', 'last_x', self.last_x, 'last_y', self.last_y, 'lParam', lParam)
        if button == "left":
            win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
            win32gui.PostMessage(self.target_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        elif button == "right":
            win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
            # win32gui.SendMessage(self.target_hwnd, win32con.WM_SETCURSOR, self.target_hwnd, win32api.MAKELONG(win32con.HTCLIENT, win32con.WM_RBUTTONDOWN))
            win32gui.PostMessage(self.target_hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)

    def send_mouse_up(self, button):
        # 模拟鼠标按键释放
        lParam = win32api.MAKELONG(self.last_x, self.last_y)
        print('鼠标抬起', 'last_x', self.last_x, 'last_y', self.last_y, 'lParam', lParam)
        if button == "left":
            win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
            win32gui.PostMessage(self.target_hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        elif button == "right":
            win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
            win32gui.PostMessage(self.target_hwnd, win32con.WM_RBUTTONUP, 0, lParam)

    def send_middle_mouse_click(self):
        # 模拟鼠标中键按下
        lParam = win32api.MAKELONG(self.last_x, self.last_y)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_MBUTTONDOWN, win32con.MK_MBUTTON, lParam)
        time.sleep(random.uniform(0.1, 0.3))

        # 模拟鼠标中键释放
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_MBUTTONUP, win32con.MK_MBUTTON, lParam)
        time.sleep(random.uniform(0.1, 0.3))

    def send_mouse_move(self, x, y, button=''):
        self.last_x = int(x)
        self.last_y = int(y)

        # 模拟鼠标移动
        lParam = win32api.MAKELONG(self.last_x, self.last_y)

        button_to_vk = {'left': win32con.MK_LBUTTON, 'right': win32con.MK_RBUTTON}

        vk = button_to_vk.get(button, 0)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_MOUSEMOVE, vk, lParam)

    def send_mouse_move_to(self, x: int, y: int, button='', duration=0.02, offset_x=5, offset_y=5,
                           insert_func = None):
        x = random.randint(x - offset_x, x + offset_x)
        y = random.randint(y - offset_y, y + offset_y)
        if x == self.last_x and y == self.last_y:
            return
        if x == self.last_x:
            x -= 1 if x > 0 else -1

        le = random.randrange(2, 4)
        t = random.randrange(1, 3)
        start = [self.last_x, self.last_y]
        end = [x, y]
        # 计算两点之间的距离
        distance = self.bezier.distance(start, end)
        # 根据距离计算点的数量
        num_points = max(int(distance / random.randint(18, 25)), 5)
        number = random.randrange(num_points, num_points + 10)

        print('start', start, 'end', end, 'distance', distance, 'num_points', num_points, number)

        track = self.bezier.trackArray(start, end, num_points, le=le, type=t)['trackArray']
        track = self.bezier.sort(start, end, track)
        # print(track)
        steps = len(track)
        for step in range(steps):
            self.send_mouse_move(track[step][0], track[step][1], button)
            if insert_func:
                insert_func(self)
            time.sleep(duration)

        time.sleep(0.01)
        # x = int(x)
        # y = int(y)
        # # 获取当前虚拟鼠标位置
        # current_x = self.last_x
        # current_y = self.last_y
        #
        # # 计算移动步数
        # steps = int(duration * 100)  # 每秒移动50步
        #
        # # 计算每步的位移量
        # delta_x = (x - current_x) / steps
        # delta_y = (y - current_y) / steps
        #
        # button_to_vk = {'left': win32con.MK_LBUTTON, 'right': win32con.MK_RBUTTON}
        #
        # vk = button_to_vk.get(button, 0)
        #
        # # 移动虚拟鼠标逐步到目标位置
        # for step in range(steps + 1):
        #     new_x = int(current_x + step * delta_x)
        #     new_y = int(current_y + step * delta_y)
        #
        #     lParam = win32api.MAKELONG(new_x, new_y)
        #     win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        #     win32gui.PostMessage(self.target_hwnd, win32con.WM_MOUSEMOVE, vk, lParam)
        #
        #     time.sleep(duration / steps)
        #
        # # 更新最后位置
        # self.last_x = x
        # self.last_y = y

    def send_middle_mouse_scroll_down(self, lines=1, delay_between_steps=0.03):
        # 模拟中键向下滚动
        tmp = win32api.MAKELONG(self.last_x, self.last_y)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        # win32gui.SendMessage(self.target_hwnd, win32con.WM_NCHITTEST, 0, tmp)
        for _ in range(lines):
            win32gui.PostMessage(self.target_hwnd, win32con.WM_MOUSEWHEEL, win32api.MAKELONG(0, -120), tmp)
            time.sleep(delay_between_steps)

    def send_middle_mouse_scroll_up(self, lines=1, delay_between_steps=0.03):
        # 模拟中键向上滚动
        # wParam = win32con.MK_MBUTTON
        # lParam = win32api.MAKELONG(self.last_x, self.last_y)
        # for _ in range(lines):
        #     win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        #     win32gui.PostMessage(self.target_hwnd, win32con.WM_MOUSEWHEEL, -120, 0)
        #     time.sleep(delay_between_steps)
        tmp = win32api.MAKELONG(self.last_x, self.last_y)
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        # win32gui.SendMessage(self.target_hwnd, win32con.WM_NCHITTEST, 0, tmp)
        # win32gui.SendMessage(self.target_hwnd, win32con.WM_SETCURSOR, self.target_hwnd,win32api.MAKELONG(win32con.HTCLIENT, win32con.WM_MOUSEWHEEL))
        for _ in range(lines):
            win32gui.PostMessage(self.target_hwnd, win32con.WM_MOUSEWHEEL, win32api.MAKELONG(0, 120), tmp)
            time.sleep(delay_between_steps)

    def send_key_down(self, key):
        # if key == 'tab':
        #     key_code = win32con.VK_TAB
        # elif key == 'shift':
        #     key_code = win32con.VK_SHIFT
        # else:
        #     key_code = keyboard.key_to_scan_codes(key)
        key_code = self.find_keycode_by_name(key)
        lParam = win32api.MAKELONG(0, win32api.MapVirtualKey(key_code, 0))
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_KEYDOWN, key_code, lParam)

    def send_key_up(self, key):
        # if key == 'tab':
        #     key_code = win32con.VK_TAB
        # elif key == 'shift':
        #     key_code = win32con.VK_SHIFT
        # else:
        #     key_code = ord(key)
        key_code = self.find_keycode_by_name(key)
        lParam = win32api.MAKELONG(0, win32api.MapVirtualKey(key_code, 0))
        win32gui.SendMessage(self.target_hwnd, win32con.WM_SETFOCUS, 0, 0)
        win32gui.PostMessage(self.target_hwnd, win32con.WM_KEYUP, key_code, lParam)

    def send_key(self, key):
        self.send_key_down(key)
        time.sleep(random.uniform(0.1, 0.2))  # 随机延时
        self.send_key_up(key)
        time.sleep(random.uniform(0.1, 0.3))  # 随机延时

    def send_enter(self):
        # 模拟回车键（按下和释放）
        self.send_key_down('\n')
        time.sleep(random.uniform(0.1, 0.3))  # 随机延时
        self.send_key_up('\n')
        time.sleep(random.uniform(0.1, 0.3))  # 随机延时

    # 定义一个函数来根据按键名称查找键码
    def find_keycode_by_name(slef, name):
        return keyname_to_keycode.get(name.lower())


class key_press(object):
    def __init__(self, msg: MessageSender, char: str):
        self.char = char
        self.msg = msg

    def __enter__(self):
        self.msg.send_key_down(self.char)
        time.sleep(random.uniform(0.2, 0.3))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        time.sleep(random.uniform(0.4, 0.6))
        self.msg.send_key_up(self.char)


class KeyPressHold(object):
    def __init__(self, msg: MessageSender, char: str):
        self.char = char
        self.msg = msg

    def __enter__(self):
        self.msg.send_key_down(self.char)
        time.sleep(random.uniform(0.2, 0.3))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        time.sleep(random.uniform(0.4, 0.6))
        self.msg.send_key_up(self.char)
