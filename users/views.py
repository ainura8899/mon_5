from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#from models import ConfirmCode
import random

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong!'})

# Create function confirm_api_view
@api_view(['POST'])
def confirm_api_view(request):
    user_id = request.data.get('user_id')
    confirmation_code = request.data.get('confirmation_code')

    # Проверка наличия user_id и confirmation_code
    if not user_id or not confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'error': 'User ID and confirmation code are required.'})

    try:
        # Проверка, существует ли код, связанный с указанным пользователем
        confirm_code = ConfirmCode.objects.get(user_id=user_id, code=confirmation_code)
    except ConfirmCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Invalid user ID or confirmation code.'})

    # Активация пользователя
    user = confirm_code.user
    user.is_active = True
    user.save()

    # Удаление использованного кода
    confirm_code.delete()

    return Response(status=status.HTTP_200_OK,
                    data={'message': 'User confirmed and activated successfully.'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, password=password, is_active=False)

    # Create code(6-symbols)
def generate_confirmation_code():
    return str(random.randint(100000, 999999))


    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
