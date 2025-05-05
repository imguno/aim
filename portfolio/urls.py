from django.urls import path
from . import views
urlpatterns = [
    path('request/', views.PortfolioRequestView.as_view(), name=''),
    path('securities_register/', views.SecuritiesRegisterView.as_view()),
    path('securities_update/', views.SecuritiesUpdatePriceView.as_view()),
    path('securities_delete/', views.SecuritiesDeleteView.as_view()),
]

