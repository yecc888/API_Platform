from django.shortcuts import render

# Create your views here.
from .models import EnvManager
from .serializers import EnvSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class EnvsListView(APIView):
    """
    List all envs
    基础VIEW
    """
    def get(self, request):
        envs = EnvManager.objects.all()
        serializer = EnvSerializer(envs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        创建环境数据
        :param request:
        :param format:
        :return:
        """
        serializer = EnvSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
