from django.urls import path
from .views import AllUsersView, SignupView, UserDetailView, SigninView

urlpatterns = [
    path("all-users/", AllUsersView.as_view(), name="all-users"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-details"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
]