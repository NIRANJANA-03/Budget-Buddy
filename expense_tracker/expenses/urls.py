from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('income/', views.income, name='income'),
    path('cat/', views.cat, name='cat'),
    path('home/', views.home, name='home'),
    path('divider/', views.divider, name='divider'),
    path('tourm/', views.tourm, name='tourm'),
    path('expense/', views.expense, name='expense'),
    path('bar/', views.bar, name='bar'),
    path('chart/', views.chart, name='chart'),
    path('header/', views.header, name='header'),
  
    
]
