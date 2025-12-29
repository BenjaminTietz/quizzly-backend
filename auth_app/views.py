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
        Creates a new user.
        
        Args:
            request (Request): Django request object
        
        Returns:
            Response: Django response object with either created user data or error data
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
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Refresh access token using refresh token from HTTP-only cookie.

        Returns:
            Response: Django response object with refreshed access token and HTTP-only cookie
        """
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
            max_age=300,
        )

        return response
    

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Authenticates user using provided username and password.

        If authentication is successful, sets HTTP-only cookies for access and refresh tokens.

        Returns:
            Response: Django response object with either authenticated user data or error data
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
        Logs out the user by deleting the access and refresh tokens.

        Returns:
            Response: Django response object with success message and 200 status code
        """
        response = Response(
            {"detail": "Logged out"},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response