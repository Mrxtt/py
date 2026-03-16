import keyword
import traceback
import logging

logging.basicConfig(level=logging.ERROR)


class User(object):
    def __init__(self, name, age):
        print("调用了 def __init__ 方法")
        self.name = name
        self.age = age

    def __get__(self, instance, value):
        print("获取name的值")
        return self.name

    # def __new__(cls, *args, **kwargs):
    #     print('调用了 def __new__ 方法')
    #     print(args)
    #     print(kwargs)
    #     return super(User, cls).__new__(cls)


class Myclass(object):
    x = User("张四", 22)


if __name__ == "__main__":
    # print(dir(User(11,22)))
    user = User("张三", 22)
    # print(user.name)

    # m = Myclass()
    # print(m.x)
    # print(keyword.kwlist)
    # print(type(m.x))
    # print(type(m))
    # print("aa", "bb", "cc")
    try:
        ss = 1 / 0
        num = "abc"
        for i in num:
            print(f"aa", "bb", "cc{}", user.name, sep="|")
        x = 0
        y = 10
        while x < y:
            print(x)
            x = x + 1
    except Exception as e:
        # print(e.args)
        # print(str(e))
        # print(repr(e))
        # err = traceback.print_exc()
        # print(err)
        logging.exception("发生异常")
