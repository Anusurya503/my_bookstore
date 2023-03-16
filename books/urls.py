from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.book_list, name='book_list'),
    path('upload/', views.book_upload, name='book_upload'),
    path('library/', views.library, name='library'),
    path('download/<int:book_id>/', views.book_download, name='book_download'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]

