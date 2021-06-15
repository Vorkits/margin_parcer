import math

def linch_dict_divider(raw_dict, num):
    list_result = []
    len_raw_dict = len(raw_dict)
    if len_raw_dict > num:
        base_num = len_raw_dict // num
        addr_num = len_raw_dict % num
        for i in range(num):
            this_dict = dict()
            keys = list()
            if addr_num > 0:
                
                keys = list(raw_dict.keys())[:base_num + 1]
                addr_num -= 1
            else:
                keys = list(raw_dict.keys())[:base_num]
            for key in keys:
                this_dict[key] = raw_dict[key]
                del raw_dict[key]
            list_result.append(this_dict)

    else:
        for d in raw_dict:
            this_dict = dict()
            this_dict[d] = raw_dict[d]
            list_result.append(this_dict)

    return list_result

