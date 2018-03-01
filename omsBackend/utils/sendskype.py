# -*- coding: utf-8 -*-
# author: itimor

from omsBackend.settings import SK


def skype_bot(user, content):
    chat = SK.chats[user]
    chat.sendMsg(content)

if __name__ == '__main__':
    for chatId in SK.chats.recent():
        print(chatId)
