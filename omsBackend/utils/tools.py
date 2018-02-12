# -*- coding: utf-8 -*-
# author: itimor

a = [{'replace': '/idc', 'value': '宇宙帝国', 'details': 'type', 'prev': None}, {'replace': '/status', 'value': 'used', 'prev': 'noused'}]


def removeNone(lst):
    diff_list = []
    for i in lst:
        yy = dict()
        yy['replace'] = i['replace']
        if i['value']:
            yy['value'] = i['value']
        else:
            yy['value'] = 'null'

        if i['prev']:
            yy['prev'] = i['prev']
        else:
            yy['prev'] = 'null'
        diff_list.append(yy)
    return diff_list

if __name__ == '__main__':
    print(removeNone(a))
