#  -*- coding: UTF-8 -*-
# author:Cuber_AHZ
# email:2119244804@qq.com

def delStr(text, not_list):
    text_ = list(text)
    use_list = delList(text_, not_list)
    return_ = list2str(use_list)
    return return_

def list2str(list_):
    return_ = ""
    for i in range(len(list_)):
        return_ = return_ + list_[i]
    return return_

def delList(list_, not_list):
    use_list = []
    for i in list_:
        if i in not_list:
            pass
        else:
            use_list.append(i)
    return use_list