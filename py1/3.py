"""
多线程
"""

import threading


def worker():
    print("子线程 native id:", threading.get_native_id())


print("主线程 native id:", threading.get_native_id())

t = threading.Thread(target=worker)
t.start()
t.join()
