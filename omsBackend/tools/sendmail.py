# -*- coding: utf-8 -*-
# author: itimor

import sys,getpass
import smtplib
from email.mime.text import MIMEText

# 发送邮件函数
def send_mail(to_list, sub,context):
       me = mail_user + "<"+mail_user+"@"+mail_postfix+">"
       #f = open(context)
       #msg = MIMEText(f.read(),_charset="utf-8")
       #f.close()
       msg = MIMEText(context)
       msg['Subject'] = sub
       msg['From'] = me
       msg['To'] = "".join(to_list)
       try:
            send_smtp = smtplib.SMTP()
            send_smtp.connect(mail_host,587)
            send_smtp.starttls()
            send_smtp.login(mail_user, mail_pass)
            send_smtp.sendmail(me, to_list, msg.as_string())
            send_smtp.close()
            return True
       except Exception as e:
            print(e)
            return False

# 设置服务器名称、用户名、密码以及邮件后缀
mail_host = "mail.tb-gaming.com"
mail_user = "oms@tb-gaming.com"
mail_pass = "u62En68D9d"    #隐藏输入密码
mail_postfix="tb-gaming.com"
#mailto_list = ["1542141838@qq.com","jjyy@qq.com"]
mailto_list = sys.argv[1]
sub= sys.argv[2]
context=sys.argv[3]

if send_mail(mailto_list,sub,context):
       print("Send mail succed!")
