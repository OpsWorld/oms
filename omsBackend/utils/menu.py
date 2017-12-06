# -*- coding: utf-8 -*-
# author: itimor

# import re
#
# g = 'CN=op,OU=tty,DC=oms,DC=com'
#
# a = re.findall("CN=(\w+)",g)
# b = re.findall("DC=(\w+)",g)
# print(a)
# print(b)


import ldap3
ldap3.Reader(c, person, '(&(member=CN=myuser_in_full_name,OU=xxx,OU=xxxxxx,DC=mydomain,DC=com)(objectClass=group))', 'dc=mydomain,dc=com').search()