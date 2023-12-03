import os
import socket
import subprocess
import time

import rpyc
import win32api
import win32con
import win32process


def find_available_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    addr, port = s.getsockname()
    s.close()
    return port


def get_ports_by_process_name(name):
    # 获取所有运行的进程
    processes = win32process.EnumProcesses()
    for pid in processes:
        try:
            # 获取进程句柄
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            # 获取进程名
            exe = win32process.GetModuleFileNameEx(handle, 0)
            # print('exe',exe)
            # 如果进程名与指定的名称匹配，获取该进程所占用的端口号
            if name in exe:
                return check_process_port(str(pid))
        except Exception as e:
            pass


def check_process_port(process_id):
    cmd = 'netstat -ano | findstr "%s"' % process_id
    result = os.popen(cmd)
    for line in result:
        if line != '':
            line = line.split()
            local_address = line[1]
            pid = line[4]
            if pid == process_id:
                return local_address.split(':')[-1]


def wait_for_service(port, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            return rpyc.connect("localhost", port).root
        except ConnectionRefusedError:
            retries += 1
            time.sleep(1)
    raise Exception(f"无法连接到端口 {port} 上的服务")


def start_ocr_server():
    paddle_port = get_ports_by_process_name('paddle_main.exe')
    easy_port = get_ports_by_process_name('easy_main.exe')

    print('paddle_port', paddle_port)
    print('easy_port', easy_port)

    if not paddle_port:
        paddle_port = find_available_port()
        # 启动 paddle OCR 服务
        subprocess.Popen(f'paddle_main/paddle_main.exe --port {paddle_port}')
        print('paddle_port', paddle_port)
    if not easy_port:
        easy_port = find_available_port()
        # 启动 easy OCR 服务
        subprocess.Popen(f'easy_main/easy_main.exe --port {easy_port}')
        print('easy_port', easy_port)

    # 继续操作 OCR 服务
    paddle_rpc = wait_for_service(paddle_port)  # rpyc.connect("localhost", paddle_port).root
    easy_rpc = wait_for_service(easy_port)  # rpyc.connect("localhost", easy_port).root
    return [paddle_rpc, easy_rpc]


def close_ocr_server(rpc_list):
    for rpc in rpc_list:
        try:
            rpc.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # image = cv2.imread('bmp/6.bmp')
    #
    # result = paddle_rpc.ocr(r'D:\project\python\game_coa\bmp\6.bmp')
    # print(result)
    # result = easy_rpc.ocr(r'D:\project\python\game_coa\bmp\6.bmp')
    # print(result)
    #
    # for rpc in rpc_list:
    #     try:
    #         rpc.close()
    #     except Exception as e:
    #         print(e)
    pass
