# -*- coding: utf-8 -*-
# author: itimor

import requests
import json
from datetime import datetime, timedelta


def whois(domain):
    url = "http://whois.xinnet.com/php/domain_seo.php?domain=%s" % domain
    html = requests.get(url).text
    d = json.loads(html)
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    create_time = datetime.strptime(d["whois_registrantDate"], UTC_FORMAT) + timedelta(hours=8)
    expire_time = datetime.strptime(d["whois_expirationDate"], UTC_FORMAT) + timedelta(hours=8)

    return {"create_time": create_time, "expire_time": expire_time}

if __name__ == '__main__':
    print(whois('itimor.com'))
