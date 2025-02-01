import profile
from django.urls import path
from .views import profile,subscription_page
from account import views

app_name = 'account'

urlpatterns = [
    path('subscription/', subscription_page, name='subscription'),
    path('profile/', profile, name='profile'),
    
]
