# -*- coding: utf-8 -*-
# author: itimor

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 设置服务器名称、用户名、密码以及邮件后缀
mail_host = "mail.tb-gaming.com"
mail_user = "oms@tb-gaming.com"
mail_pass = "u62En68D9d"  # 隐藏输入密码
mail_postfix = "tb-gaming.com"
# mailto_list = ["1542141838@qq.com","jjyy@qq.com"]

# 发送邮件函数
def send_mail(to_list, cc_list, sub, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    # f = open(context)
    # msg = MIMEText(f.read(),_charset="utf-8")
    # f.close()
    #msg = MIMEText(context)
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list + ';'
    msg['Cc'] = cc_list
    list = msg['To']  + msg['Cc']
    html = """
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>工单通知邮件</title>
    <body>
    <div id="container">
    <h1>工单通知邮件</h1>
    <a href='""" + content + """'>点我查看工单</a>
    </div>
    </body>
    </html>"""
    context = MIMEText(html, _subtype='html', _charset='utf-8')  # 解决乱码
    msg.attach(context)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host, 587)
        send_smtp.starttls()
        send_smtp.login(mail_user, mail_pass)
        print(msg.as_string())

        send_smtp.sendmail(me, list, msg.as_string())
        send_smtp.close()
        return {"code":'success',"msg":"通知邮件发送成功"}
    except Exception as e:
        print(e)
        return {"code":'error',"msg":"通知邮件发送失败"}

if __name__ == '__main__':
    to_list = sys.argv[1]  # 收件人列表   '111@126.com'
    cc_list = sys.argv[2].replace(',', ';')  # 抄送人列表   '111@126.com;222@126.com;'
    sub = sys.argv[3]
    context = sys.argv[4]
    if send_mail(to_list, cc_list, sub, context):
        print({"code":'success',"msg":"通知邮件发送成功"})
    else:
        print({"code":'error',"msg":"通知邮件发送失败"})