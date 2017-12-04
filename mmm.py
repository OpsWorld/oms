# -*- coding: utf-8 -*-
# author: itimor

import re

g = 'CN=op,OU=tty,DC=oms,DC=com'

a = re.findall("CN=(\w+)",g)
b = re.findall("DC=(\w+)",g)
print(a)
print(b)