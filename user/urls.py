from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name=''),
    path('signin/', views.SigninView.as_view(), name=''),
    path('signout/', views.SignoutView.as_view(), name=''),
    path('sign_history/', views.SignHistoryView.as_view(), name=''),
    
]

