from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserCreateView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("logout/", views.UserLogoutView.as_view()),
    path("<str:username>/", views.UserProfileView.as_view()),
    path("<str:username>/blind/", views.BlindReporter.as_view()),
    path("<str:username>/unblind/", views.UnblindReporter.as_view()),
]
