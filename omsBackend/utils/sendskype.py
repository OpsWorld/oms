# -*- coding: utf-8 -*-
# author: itimor

from skpy import Skype
from omsBackend.settings import SK_ACOUNT

#登录skype
sk = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])

def skype_bot(user, content):
    print(content)
    chat = sk.chats[user]
    chat.sendMsg(content)

if __name__ == '__main__':
    for chatId in sk.chats.recent():
        print(chatId)
