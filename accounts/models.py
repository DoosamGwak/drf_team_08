from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICE_GENDER = [
        ("M", "남자"),
        ("W", "여자"),
    ]

    first_name = None
    last_name = None

    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    birthday = models.DateField()
    image = models.ImageField(upload_to="images/", default="images/default_user.png")
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)

    introduction = models.TextField(blank=True)
