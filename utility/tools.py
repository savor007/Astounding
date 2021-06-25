import time
import math
import datetime

def get_datetimestring():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


if __name__ == '__main__':
    print(get_datetimestring())
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))