from django.urls import path
from . import views
urlpatterns = [
    path('balance/', views.BalanceView.as_view(), name=''),
    path('deposit/', views.DepositView.as_view(), name=''),
    path('withdraw/', views.WithdrawView.as_view(), name=''),
    path('history/', views.BalanceHistoryView.as_view(), name='')
]