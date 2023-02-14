import logging

# 创建一个日志记录器
loger = logging.getLogger('applog')

# 设置日志记录器的等级 INFO
loger.setLevel(logging.INFO)


def configLog(isDebug=False):
    if isDebug:
        return
    print(f'log打印到文件中')
    # 创建一个将流式的日志处理器
    steram_handler = logging.StreamHandler()

    # loger.removeHandler()  #接触绑定

    # 创建一个 输出到磁盘文件的日志处理器
    file_handler = logging.FileHandler(filename='file.log', mode='w', encoding='utf-8')

    # file_handler 设置日志等级为 ERROR ,没有给handler 设置日志级别,该handler 将使用logger设置或者默认的级别
    file_handler.setLevel(logging.ERROR)

    # 创建一个日志格式器
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -%(module)s:::  %(message)s")

    # 设置处理器输出的日志格式
    file_handler.setFormatter(formatter)
    steram_handler.setFormatter(formatter)

    # 设置一个过滤器
    fl1 = logging.Filter('app2log')

    # 给日志记录器设置一个过滤器 ,(从根部开始过滤)
    # loger.addFilter(fl1)

    # 还可以给 handler 设置过滤器 (在输出的时候过滤)
    steram_handler.addFilter(fl1)

    # 记录器设置一个处理器
    loger.addHandler(steram_handler)
    loger.addHandler(file_handler)
