from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status,generics,serializers
from .models import Users
from .serializers import UserSerializer,UserLoginSerializer,AdminLoginSerializer

# Create your views here.
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        Users.objects.create(user=user, role='trader')
        return Response({
            'message':"User successfully created",
            'username':user.username,
        },status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminLoginSerializer