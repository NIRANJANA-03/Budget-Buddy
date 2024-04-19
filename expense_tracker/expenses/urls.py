from . import views
from django.urls import path
from .views import DownloadPDF 

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('forgot/', views.forgot, name='forgot'),

    path('income/', views.income, name='income'),
    path('cat/', views.cat, name='cat'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    
    path('expense/', views.expense, name='expense'),
    path('bar/', views.bar, name='bar'),
    path('chart/', views.chart, name='chart'),
    path('header/', views.header, name='header'),
    path('download-pdf/', DownloadPDF.as_view(), name='download_pdf'),

    path('hometour/', views.hometour, name='hometour'),
    path('cattour/', views.cattour, name='cattour'),
    path('addtour/', views.addtour, name='addtour'),
    #path('maintour/', views.maintour, name='maintour'),
    path('maintour/<str:tour_name>/', views.maintour, name='maintour'),
    path('update_status/<str:tour_name>/', views.update_status, name='update_status'),

    path('divider/<str:event_name>/', views.divider, name='divider'),
    path('eventhome/', views.eventhome, name='eventhome'),
    path('eventadd/', views.eventadd, name='eventadd'),
    path('eventcat/', views.eventcat, name='eventcat'),
    path('close_event/<str:event_name>/', views.close_event, name='close_event'),
    path('send_report/<str:event_name>/', views.send_report, name='send_report'),
]
