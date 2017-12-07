# -*- coding: utf-8 -*-
# author: itimor

a = [
    {
        "path": '/worktickets',
        "name": '工单管理',
        "icon": 'list',
        "children": [
            {"path": 'workticket', "name": '工单列表'},
            {"path": 'tickettype', "name": '工单类型'},
        ]
    },
    {
        "path": '/users',
        "name": '用户管理',
        "icon": 'user',
        "children": [
            {"path": 'user', "name": '用户列表'},
            {"path": 'group', "name": '组类型'},
        ]
    },
    {
        "path": '*',
        "name": '不存在',
    }
]

b = [
    {
        "name": '工单管理',
        "children": [
            {"name": '工单列表'},
        ]
    },
    {
        "path": '*',
        "name": '不存在',
    }
]

c = []
for i in a:
    for j in b:
        if i["name"] == j["name"]:
            d = []
            try:
                for m in i["children"]:
                    for n in j["children"]:
                        if m["name"] == n["name"]:
                            d.append(m)
                i["children"] = d
            except:
                pass
            finally:
                c.append(i)
print(c)