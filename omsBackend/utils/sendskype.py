# -*- coding: utf-8 -*-
# author: itimor

from skpy import Skype

sk_user = 'tbkiven@outlook.com'
sk_pass = 'tengfa9188'
sk_group = 'chat group'
sk_touser = 'larry'
content = "hello"

sk = Skype(sk_user, sk_pass)

user_dict = {
    'larry': '8:larry16898',
    'tbitsupport': '8:tbitsupport01'
}

def skype_bot(to_user, content):
    chat = sk.chats[user_dict[to_user]]
    chat.sendMsg(content)


if __name__ == '__main__':
    for chatId in sk.chats.recent():
        print(chatId)
