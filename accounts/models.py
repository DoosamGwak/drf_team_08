from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICE_GENDER = [
        ("M", "남자"),
        ("W", "여자"),
    ]
    first_name = None
    last_name = None
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50) #실명
    nickname = models.CharField(max_length=50) #별명
    birthday = models.DateField()
    image = models.ImageField(upload_to="images/", default="images/default_user.png")
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)
    introduction = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Blind(models.Model):
    blinder = models.ForeignKey(User, related_name='blinding', on_delete=models.CASCADE)
    blinded = models.ForeignKey(User, related_name='blinders', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blinder', 'blinded')  # 중복 방지

    def __str__(self):
        return f"{self.blinder} blinds {self.blinded}"