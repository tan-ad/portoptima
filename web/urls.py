from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_portfolio, name='analyze_portfolio'),
    path('results/<str:analysis_id>/', views.results, name='results'),
    path('api/portfolio/analyze/', views.analyze_portfolio_api, name='analyze_portfolio_api'),
]
