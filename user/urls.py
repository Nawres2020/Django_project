from django.urls import path
from .views import home, profile, RegisterView , registration_under_review



urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('registration_under_review/', registration_under_review, name='registration_under_review'),

]
