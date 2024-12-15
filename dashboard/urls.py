from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.dashboard_home, name='dashboard_home'),
    path('blog-analysis', views.analytics_view, name='analytics_view'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),

     path('password-reset/', views.reset_password_view, name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='password_reset_done'),
 
    path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'),
    name='password_reset_confirm'),


    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='password_reset_complete'),


    path('blog-table/', views.blog_table, name='blog_table'),
    path('add-blog/', views.create_post, name='create_post'),
    path('admin-users/', views.user_table, name='user_table'),
    path('categories/', views.category_table, name='category_table'),
    path('categories/add/', views.create_category, name='create_category'),
    path('edit-post/edit/<slug:slug>/', views.edit_blogpost, name='edit_blogpost'),
    path('blogpost/<slug:slug>/delete/', views.delete_blogpost, name='delete_blogpost'),

    path('categories/<slug:slug>/edit/', views.edit_category, name='edit_category'),
    path('categories/<slug:slug>/delete/', views.delete_category, name='delete_category'),


]


