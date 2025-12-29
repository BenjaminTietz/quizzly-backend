from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}    
        }
        
    def create(self, validated_data):
        """
        Create a new user based on validated data.

        The validated data should contain the following information:
        - username
        - email
        - password
        - confirmed_password

        The confirmed_password field is not stored in the database,
        it is only used to verify that the user has entered the correct
        password.

        Returns a User object representing the newly created user.
        """
        validated_data.pop('confirmed_password', None)
        user = User.objects.create_user(**validated_data)
        return user
    

class RefreshTokenSerializer(serializers.Serializer):
    def validate(self, attrs):
        """
        Validate refresh token from HTTP-only cookie.

        :param attrs: Dictionary containing validated data
        :return: Validated data with refresh token added
        :raises AuthenticationFailed: If refresh token is missing
        """
        request = self.context.get("request")
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token missing")

        attrs["refresh_token"] = refresh_token
        return attrs
