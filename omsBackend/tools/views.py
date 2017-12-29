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
    queryset = Upload.objects.all()
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

        cc = request.data["cc"]
        cc_list = ''
        if cc:
            for c in cc.split(','):
                try:
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
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SendmessageViewSet(viewsets.ModelViewSet):
    queryset = Sendmessage.objects.all()
    serializer_class = SendmessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = SendmessageSerializer(data=request.data, context={'request': request})
        content = request.data["title"] + '\n' + request.data["message"]
        print(content)
        try:
            create_user = request.data["create_user"]
            to_create_user = User.objects.get(username=create_user).skype
            send_to_skype.delay(to_create_user,content)
            action_user = request.data["action_user"]
            to_action_user = User.objects.get(username=action_user).skype
            send_to_skype.delay(to_action_user, content)
        except Exception as e:
            print(e)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"xxoo"}, status=status.HTTP_201_CREATED)