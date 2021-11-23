from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from knox.models import AuthToken, User
from rest_framework.serializers import Serializer
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.views.decorators.csrf import csrf_exempt
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

@api_view(["POST"])
@csrf_exempt
def login_view_api(request, *args, **kwargs):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        username = data['username']
        password = data['password']
        authUser = authenticate(request, username=username, password=password)
        if authUser:
            login(request, authUser)
            user = User.objects.filter(username=username).first()
            print("user: ", user)
            _, token = AuthToken.objects.create(authUser)
            
            return Response({"token": token}, status=200)
    return Response({})


@api_view(['PUT',])
def user_api_update_view(request):
    qs = User.objects.filter(username=request.user)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if request.method == 'PUT':
        serializer = UserSerializer(obj,data=request.data, context={"request":request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Profile has been successfully upated."
            return Response(serializer.data,200)
    return Response(serializer.errors, status=400)

class LoginApi(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny, 
    ]
    serializer_class = LoginSerializer
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print("request: ",request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            authUser = authenticate(request,username=username, password=password)
            print("authUser: ",authUser)
            if authUser:
                user = login(request, authUser)
                print("user: ", user)
                _, token = AuthToken.objects.create(authUser)
                return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token
                })
            else:
                return Response({"incorrect cridentials"})
        return Response({})

class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated, 
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user