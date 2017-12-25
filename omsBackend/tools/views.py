# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from tools.models import Upload, Sendmail, Sendmessage
from tools.serializers import UploadSerializer, SendmailSerializer, SendmessageSerializer
from tools.filters import UploadFilter
from users.models import User
from utils.sendmail import send_mail
from utils.sendskype import skype_bot

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
        results = send_mail(to_list, cc_list, sub, content)
        print(results)
        #cmd = '/root/.pyenv/versions/envoms/bin/python /data/projects/oms/omsBackend/utils/sendmail.py {} {} {} {}'.format(to_list, cc_list, sub, content)
        #print(cmd)
        #results = run(cmd).stdout
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SendmessageViewSet(viewsets.ModelViewSet):
    queryset = Sendmessage.objects.all()
    serializer_class = SendmessageSerializer
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = SendmessageSerializer(data=request.data, context={'request': request})
    #     to_user = request.data["user"]
    #     content = request.data["title"] + '\n' + request.data["message"]
    #     skype_bot(to_user,content)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)