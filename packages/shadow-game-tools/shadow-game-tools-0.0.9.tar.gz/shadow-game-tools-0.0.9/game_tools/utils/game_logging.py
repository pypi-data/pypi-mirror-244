import logging

# 创建一个日志器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建一个处理器，用于写入日志文件
handler = logging.FileHandler('example.log')

# 创建一个格式器，用于添加日志信息的格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式器设置到处理器上
handler.setFormatter(formatter)

# 将处理器添加到日志器上
logger.addHandler(handler)
