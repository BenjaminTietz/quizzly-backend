from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        """
        Returns the username of the user as a string.

        :return: The username of the user
        :rtype: str
        """
        return self.username