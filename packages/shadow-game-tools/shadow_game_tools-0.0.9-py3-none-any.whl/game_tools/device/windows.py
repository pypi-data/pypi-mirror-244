import win32gui
import ctypes
import re


def lock_window(hwnd):
    # 禁用窗口的键盘和鼠标事件
    ctypes.windll.user32.EnableWindow(hwnd, False)
    # ctypes.windll.user32.BlockInput(True)


def unlock_window(hwnd):
    # 恢复窗口的键盘和鼠标事件
    ctypes.windll.user32.EnableWindow(hwnd, True)
    # ctypes.windll.user32.BlockInput(False)


def find_window_handles(window_class, window_title_pattern, window_child_class):
    result = []

    def enum_windows_callback(handle, data):
        window_title = win32gui.GetWindowText(handle)
        if win32gui.GetClassName(handle) == window_class and re.search(window_title_pattern, window_title,re.IGNORECASE):
            result.append(handle)

        return True  # 继续枚举其他窗口

    win32gui.EnumWindows(enum_windows_callback, None)

    window_handles_with_children = []

    for handle in result:
        child_handles = []

        def enum_child_windows_callback(child_handle, child_data):
            # child_window_title = win32gui.GetWindowText(child_handle)
            if win32gui.GetClassName(child_handle) == window_child_class:
                child_handles.append(child_handle)
            return True

        win32gui.EnumChildWindows(handle, enum_child_windows_callback, None)
        window_handles_with_children.append([handle, child_handles])

    return window_handles_with_children


def _main():
    hwnd = 263674

    print("锁定窗口")
    lock_window(hwnd)

    input('123123')

    print("解锁窗口")

    unlock_window(hwnd)


if __name__ == "__main__":
    window_title_pattern = r".*TigerVnc"
    window_class = 'vncviewer'
    window_child_class = ''
    hwnd = find_window_handles(window_class, window_title_pattern,window_child_class)
    print(hwnd)