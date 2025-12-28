from django.shortcuts import render
from rest_framework.views import APIView

from auth_app.authentication import CookieJWTAuthentication
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import RefreshTokenSerializer
from .utils import refresh_access_token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    

    def post(self, request):
        """
        Registers a new user with the given data.

        Args:
            request: The incoming request.

        Returns:
            Response: A response containing the registered user data if successful, otherwise an error response.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RefreshTokenView(APIView):
    """
    Refresh access token using refresh token from HTTP-only cookie.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RefreshTokenSerializer(
            data={}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        access_token = refresh_access_token(
            serializer.validated_data["refresh_token"]
        )

        response = Response(
            {
                "detail": "Token refreshed",
                "access": access_token,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60,
        )

        return response
    

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Authenticates a user using the given credentials and returns an access token and a refresh token.

        Args:
            request: The incoming request.

        Returns:
            Response: A response containing the access token and refresh token if successful, otherwise an error response.
        """
        
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response(
            {"detail": "Login successful", 
             "access": access,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,  
            samesite="None",
            max_age=300,
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,  
            samesite="None",
            max_age=86400,
        )

        return response
    

class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Logs out the user by deleting the access token and refresh token cookies.

        Returns:
            Response: A response with a status of 200 OK.
        """
        response = Response(
            {"detail": "Logged out"},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response