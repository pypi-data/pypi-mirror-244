#  -*- coding: UTF-8 -*-
# author:Cuber_AHZ
# email:2119244804@qq.com

def strr(content):
    """
    `strr`用于将STR转STR:
        "'str'" --> 'str'
    :param content:
        需要转STR的内容
    """

    # 输出的str
    str_return = None

    if len(content) >= 2:

        # 由str转成的list
        str_to_list = list(content)

        try:
            if len(str_to_list) >= 6:

                # 前三和后三
                str_to_list_T = str_to_list[0] + str_to_list[1] + str_to_list[2]
                str_to_list_t = str_to_list[-1] + str_to_list[-2] + str_to_list[-3]

                # 当前三后三为"""|'''
                if str_to_list_T == '"""' and str_to_list_t == '"""' or str_to_list_T == "'''" and str_to_list_t == "'''":
                    str_return = ""
                    for i in range(3):
                        del str_to_list[0]
                        del str_to_list[-1]
                    for i in str_to_list:
                        str_return = str_return + i

                # 当前后为'
                elif str_to_list[0] == "'" and str_to_list[-1] == "'" or str_to_list[0] == '"' and str_to_list[-1] == '"':
                    str_return = ""
                    del str_to_list[0]
                    del str_to_list[-1]
                    for i in str_to_list:
                        str_return = str_return + i

            # 当前后为"
            elif str_to_list[0] == "'" and str_to_list[-1] == "'" or str_to_list[0] == '"' and str_to_list[-1] == '"':
                str_return = ""
                del str_to_list[0]
                del str_to_list[-1]
                for i in str_to_list:
                    str_return = str_return + i

        except:
            pass

    return str_return

def intr(content):
    """
    `intr`用于将STR转INT(不能转负整数):
        "1" --> 1
    :param content:
        需要转INT的内容
    """

    # 返回的int
    int_return = None

    # 可以int
    try:
        if content.isdigit():
            int_return = int(content)
    except:
        pass

    return int_return

def boolr(content):
    """
    `boolr`用于将STR转BOOL:
        "True" --> True
    :param content:
       需要转BOOL的内容
    """

    # 返回的bool
    bool_return = None

    # 为"True"|"False"
    if content == "True":
        bool_return = True
    elif content == "False":
        bool_return = False

    return bool_return

def floatr(content):
    """
    `floatr`用于将STR转FLOAT:
        "1.0" --> 1.0
    :param content:
        需要转FLOAT的内容
    """

    # 返回的float
    float_return = None

    # 可以float
    try:
        float_return = float(content)
    except:
        float_return = None
    return float_return

def listr(content):
    """
    `listr`用于将STR转LIST:
        '[1,"str"]' --> [1,"str"]
        '["s",["dd","dd"]]' --> ["s",["dd","dd"]]

    :param content:
        需要转LIST的内容
    """
    # 返回的list
    list_return = None
    # 用于处理
    list_in = None
    # 函数循环次数
    t_count = 0
    # 处理list中的str
    str_in_list = ""
    # 删除的次数
    list_del_count = 0

    if len(content) >= 2:
        # 由str转成的list
        str_to_list = list(content)

        if str_to_list[0] == "[":
            list_del_count = 1
            del str_to_list[0]
            list_return = []

            while True:
                if len(str_to_list) == 0:
                    break

                # LIST[LIST[...]]([)
                if str_to_list[0] == "[":
                    # listr获取的list
                    list_of_listr = None
                    # listr获取的删除数
                    count_of_listr = 0
                    # 用for循环将str_to_list合并成的str
                    for_to_get_list = ""

                    for i in str_to_list:
                        for_to_get_list = for_to_get_list + i
                        list_of_listr, count_of_listr = listr(for_to_get_list)
                    list_return.append(list_of_listr)

                    for i in range(count_of_listr):
                        if len(str_to_list) == 0:
                            break
                        list_del_count += 1
                        del str_to_list[0]

                # LIST[STR](")
                try:
                    # 开头为"
                    if str_to_list[0] == '"':
                        list_in = []

                        # 循环获取内容（将str_tp_list的第一项加入list_in）
                        while True:
                            list_in.append(str_to_list[0])
                            list_del_count += 1
                            del str_to_list[0]

                            # 再次为"，将list_in改str
                            if str_to_list[0] == '"':
                                str_in_list = ""
                                for i in list_in:
                                    str_in_list = str_in_list + i

                                # strr
                                str_in_list = str_in_list + '"'
                                str_in_list = strr(str_in_list)
                                list_return.append(str_in_list)
                                list_del_count += 1
                                del str_to_list[0]
                                break
                except:
                    pass

                # LIST[STR](')
                try:
                    # 开头为'
                    if str_to_list[0] == "'":
                        list_in = []

                        # 循环获取内容（将str_tp_list的第一项加入list_in）
                        while True:
                            list_in.append(str_to_list[0])
                            list_del_count += 1
                            del str_to_list[0]

                            # 再次为'，将list_in改str
                            if str_to_list[0] == "'":
                                str_in_list = ""
                                for i in list_in:
                                    str_in_list = str_in_list + i

                                # strr
                                str_in_list = str_in_list + "'"
                                str_in_list = strr(str_in_list)
                                list_return.append(str_in_list)
                                list_del_count += 1
                                del str_to_list[0]
                                break
                except:
                    pass

                # LIST[INT|FLOAT]
                try:
                    # 为数字
                    if str_to_list[0].isdigit():
                        list_in = []
                        # 获得的数字
                        int_get = 0
                        # 位数
                        int_count = 1

                        while True:
                            # 如果是"],."("]"退出，","退出，"."小数float)
                            if str_to_list[0] == "]" or str_to_list[0] == "," or str_to_list[0] == ".":
                                for i in list_in:
                                    int_get = int_get + int_count * i
                                    int_count = int_count * 10

                                    if str_to_list[0] == ".":
                                        a_ = str(int_get)
                                        list_del_count += 1
                                        del str_to_list[0]
                                        int_get = 0
                                        int_count = 1
                                        list_in.clear()

                                        while True:
                                            if str_to_list[0] == "]" or str_to_list[0] == ",":
                                                for i in list_in:
                                                    int_get = int_get + int_count * i
                                                    int_count = int_count * 10
                                                a_ = a_ + "." + str(int_get)
                                                int_get = floatr(a_)
                                                break

                                            if str_to_list[0].isdigit():
                                                list_in.append(int(str_to_list[0]))
                                                list_del_count += 1
                                                del str_to_list[0]
                                                list_return.append(int_get)
                                                break

                            # 为数字(int)
                            if str_to_list[0].isdigit():
                                list_in.insert(0, int(str_to_list[0]))
                                list_del_count += 1
                                del str_to_list[0]
                except:
                    pass

                # LIST[BOOL]
                try:
                    if str_to_list[0] + str_to_list[1] + str_to_list[2] + str_to_list[3] == "True":
                        list_return.append(boolr(str_to_list[0] + str_to_list[1] + str_to_list[2] + str_to_list[3]))
                        for i in range(4):
                            list_del_count += 1
                            del str_to_list[0]

                    elif str_to_list[0] + str_to_list[1] + str_to_list[2] + str_to_list[3] + str_to_list[4] == "False":
                        list_return.append(boolr(str_to_list[0] + str_to_list[1] + str_to_list[2] + str_to_list[3] + str_to_list[4]))
                        for i in range(5):
                            list_del_count += 1
                            del str_to_list[0]
                except:
                    pass

                # 检查
                if t_count == 100000:
                    list_return = None
                    break
                if len(str_to_list) <= 1:
                    break
                if str_to_list[0] == "]":
                    break

                if str_to_list[0] == ",":
                    list_del_count += 1
                    del str_to_list[0]
                    if len(str_to_list) > 0:
                        if str_to_list[0] == " ":
                            list_del_count += 1
                            del str_to_list[0]
                t_count += 1
    return list_return, list_del_count

def everyr(content):
    """
    `everyr`用于将STR转换

    :param content:
        需要转换的内容
    """
    a_ = None
    a_ = strr(content)
    if a_ == None:
        a_ = intr(content)
        if a_ == None:
            a_ == floatr(content)
            if a_ == None:
                a_ = boolr(content)
                if a_ == None:
                    a_, _ = listr(content)
                    if a_ == None:
                        print('\033[1;31;1m'"RTError: Can't Return [Return None]"+"\033[1;39;1m")
    return a_
