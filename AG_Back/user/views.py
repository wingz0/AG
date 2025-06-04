from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, logout 

from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser 

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user) 

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user) 
        token, created = Token.objects.get_or_create(user=user) 
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'token': token.key 
        })

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete() 
        logout(request) 
        return Response(status=status.HTTP_204_NO_CONTENT) 
