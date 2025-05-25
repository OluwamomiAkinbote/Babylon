from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard and Analytics
    path('', views.dashboard_home, name='dashboard_home'),
    
    path('blog-analysis', views.analytics_view, name='analytics_view'),

    # User authentication
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),

    # Blog management
    path('blog-table/', views.blog_table, name='blog_table'),
    path('add-blog/', views.create_post, name='create_post'),
    path('edit-post/edit/<slug:slug>/', views.edit_blogpost, name='edit_blogpost'),
    path('blogpost/<slug:slug>/delete/', views.delete_blogpost, name='delete_blogpost'),

    # Category management
    path('categories/', views.category_table, name='category_table'),
    path('categories/add/', views.create_category, name='create_category'),
    path('categories/<slug:slug>/edit/', views.edit_category, name='edit_category'),
    path('categories/<slug:slug>/delete/', views.delete_category, name='delete_category'),

    # Password reset
    path('password-reset/', views.reset_password_view, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='password_reset_complete'),
]
