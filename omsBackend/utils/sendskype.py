# -*- coding: utf-8 -*-
# author: itimor

from skpy import Skype

sk_user = 'tbkiven@outlook.com'
sk_pass = 'tengfa9188'
sk_group = 'chat group'
sk_touser = 'larry'
content = "hello"

sk = Skype(sk_user, sk_pass)

chat_dict = {
    '运维组': '19:1f93a089523f4889843e926106822721@thread.skype',
    'tbitsupport': '8:tbitsupport01'
}

def skype_bot(user, content):
    print(user)
    chat = sk.chats[chat_dict['运维组']]
    chat.sendMsg(content)

if __name__ == '__main__':
    for chatId in sk.chats.recent():
        print(chatId)
