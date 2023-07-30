from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication 
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST', 'GET'])
def signup(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.favoriteGenres)
        return Response(serializer)
    else:
        password = request.data.get('password')
        password_confirmation = request.data.get('passwordConfirmation')
            
        if password != password_confirmation:
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_username(request):
    is_super =False
    if(request.user.is_superuser):
        is_super = True
    favorite = request.user.favoriteGenres.split()
    new_dict = {
        'username' : request.user.username,
        'user_id' : request.user.id, 
        'favorite_genres': favorite,
        'is_superuser' : is_super,
        }
    return Response(new_dict)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def identify_user_superuser(request):
    is_super =False
    if(request.user.is_superuser):
        is_super = True
    new_dict = {'is_superuser' : is_super,}
    return Response(new_dict)
