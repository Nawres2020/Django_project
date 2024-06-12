from django.urls import path
from .views import home, profile, RegisterView , registration_under_review , logout_user 



urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('registration_under_review/', registration_under_review, name='registration_under_review'),

]
