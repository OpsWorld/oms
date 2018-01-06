# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from tools.models import Upload, Sendmail, Sendmessage
from tools.serializers import UploadSerializer, SendmailSerializer, SendmessageSerializer
from tools.filters import UploadFilter
from users.models import User
from tasks.tasks import send_to_skype, send_to_mail

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by("-create_time")
    serializer_class = UploadSerializer
    filter_class = UploadFilter


class SendmailViewSet(viewsets.ModelViewSet):
    queryset = Sendmail.objects.all()
    serializer_class = SendmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = SendmailSerializer(data=request.data, context={'request': request})
        to = request.data["to"]
        try:
            to_list = User.objects.get(username=to).email
        except Exception as e:
            to_list = 'itsupport@tb-gaming.com'
        if not to_list:
            to_list = 'itsupport@tb-gaming.com'

        cc = set(request.data["cc"].split(','))
        cc_list = ''
        try:
            for c in cc:
                if c:
                    c_email = User.objects.get(username=c).email
                    cc_list = cc_list + c_email + ','
        except Exception as e:
                cc_list = cc_list
        sub = request.data["sub"]
        content = request.data["content"]
        send_to_mail.delay(to_list, cc_list, sub, content)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "1024"}, status=status.HTTP_201_CREATED)


class SendmessageViewSet(viewsets.ModelViewSet):
    queryset = Sendmessage.objects.all()
    serializer_class = SendmessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = SendmessageSerializer(data=request.data, context={'request': request})
        content = request.data["title"] + '\n' + request.data["message"]
        action_users = set(request.data["action_user"].split(','))
        print(action_users)
        try:
            for action_user in action_users:
                if action_user:
                    to_action_user = User.objects.get(username=action_user).skype
                    print(to_action_user)
                    send_to_skype.delay(to_action_user, content)
        except Exception as e:
            print(e)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"1024"}, status=status.HTTP_201_CREATED)
