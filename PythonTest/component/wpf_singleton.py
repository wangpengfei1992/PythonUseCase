"""
coding:utf-8
@Software:PyCharm
@Time:2023/3/10 17:44
@Author:王鹏飞
单例示例
"""


class MySingleton(object):
    # 记录第一个被创建对象的引用
    instance = None
    # 记录是否执行过初始化动作
    isInit = False

    def __new__(cls, *args, **kwargs):
        # 1. 判断类属性是否是空对象
        if cls.instance is None:
            # 2. 调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        # 3. 返回类属性保存的对象引用
        return cls.instance

    def __init__(self):
        if not MySingleton.isInit:
            print(f"初始化MySingleton对象")
            MySingleton.isInit = True

    def myMethon(self):
        print(f"测试单例方法")