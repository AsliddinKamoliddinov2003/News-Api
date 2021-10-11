from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import response
from rest_framework.authtoken.views import ObtainAuthToken
from yangi_api.models import News
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  serializers, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


from .serializers import *


class NewsApiView(APIView):
    serializer_class = NewsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        news = News.objects.all()

        title = request.GET.get("title", None)
        content = request.GET.get("content", None)

        if title:
            title = news.filter(title__contains=title)

        if content:
            content = news.filter(content__contains=content)

        news_serialized = NewsSerializer(news, many=True)   
        return Response(news_serialized.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        news_serialized = NewsSerializer(data=request.data)
        if news_serialized.is_valid():
            news_serialized.save()
            return Response({"method":request.method}, status=status.HTTP_201_CREATED)
        
        return Response(news_serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class SingleNewsApiView(APIView):
    serializer_class = NewsSerializer
    
    def get(self, request, pk=None, *args, **kwargs):
        news = News.objects.get(id=pk)
        news_serialized = NewsSerializer(news, many=False)

        return Response(news_serialized.data, status=status.HTTP_200_OK)


    def put(self, request, pk=None, *args, **kwargs):
        news = News.objects.get(id=pk)
        news_serialized = NewsSerializer(instance=news, data=request.data)
        if news_serialized.is_valid():
            news_serialized.save()
            return Response( status=status.HTTP_202_ACCEPTED)

        return Response(news_serialized.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
    def patch(self, request, pk=None, *args, **kwargs):
        news = News.objects.get(id=pk)
        news_serialized = NewsSerializer(instance=news, data=request.data, partial=True)
        if news_serialized.is_valid():
            news_serialized.save()
            return Response( status=status.HTTP_202_ACCEPTED)

        return Response(news_serialized.errors, status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None, *args, **kwargs):
        news = News.objects.get(id=pk)
        news_serialized = NewsSerializer(news, many=False)
        data = news_serialized.data
        news.delete()

        return Response(data, status=status.HTTP_204_NO_CONTENT)


User = get_user_model()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = User.objects.filter(username=username)
            if user.exists():
                user = user.first()
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "token":token.key,
                        "username":username,
                        "password":password,
                        "fullname":user.fullname
                    })
                    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






    
    
