# -*- coding: utf-8 -*-
# author: itimor

from skpy import Skype

sk_user = 'oms@tb-gaming.com'
sk_pass = 'tengfa@918'
sk_group = 'chat group'
sk_touser = 'larry'
content = "hello"

sk = Skype(sk_user, sk_pass)

def skype_bot(user, content):
    #chat = sk.chats[user]
    chat = sk.chats['8:live:tbkiven']
    chat.sendMsg(content)

if __name__ == '__main__':
    for chatId in sk.chats.recent():
        print(chatId)
