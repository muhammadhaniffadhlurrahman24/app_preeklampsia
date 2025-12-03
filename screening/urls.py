from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('logout/', views.logout_view, name='logout'),
    path('screening/', views.screening_view, name='screening'),
    path('submit/', views.submit_screening, name='submit_screening'),
    path('result/', views.result_view, name='result'),
    path('download/', views.download_result, name='download_result'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
