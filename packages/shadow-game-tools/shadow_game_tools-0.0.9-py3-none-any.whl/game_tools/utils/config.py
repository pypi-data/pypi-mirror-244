import configparser


# 写入配置文件
def write_config(filename, section, settings):
    config = configparser.ConfigParser()
    config[section] = settings
    with open(filename, 'w') as configfile:
        config.write(configfile)


# 读取配置文件
def read_config(filename, section):
    config = configparser.ConfigParser()
    config.read(filename)
    if section in config:
        return config[section]
    else:
        return None
