import time

if __name__ == '__main__':
    struct_time1 = time.localtime(time.time())
    print(type(struct_time1))
    print(struct_time1)
    struct_time2 = time.localtime(1694229027)
    print(struct_time2)

    str_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time1)
    print(str_time)

    str_time = "2023-03-03 21:34:00"
    struct_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    print(struct_time)

    print(time.mktime(struct_time))
