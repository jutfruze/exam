from django.urls import path

from . import views

#ссылки
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('application/new/', views.new_application, name='new_application'),
    path('review/<int:application_id>/', views.add_review, name='add_review'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/status/<int:application_id>/', views.change_status, name='change_status'),
]
