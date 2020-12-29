from django.urls import path
from CRM_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('register/', views.registerPage,name='register'),
     path('login/',views.loginPage, name='login'),
     path('logout/',views.logoutUser, name='logout'),

     path('',views.Home,name='Home'),
     path('user/',views.userPage, name= 'user-page'),

     path('account/',views.accountSetting,name='account'),

     path('product/',views.product,name='product'),
     path('customer/<str:pk>/',views.customer,name='customer'),
     path('order_form/<str:pk>/',views.order_form,name='order_form'),
     path('updateOrder/<str:pk>/',views.updateOrder,name='updateOrder'),
     path('deleteOrder/<str:pk>/',views.deleteOrder,name='deleteOrder'),

      path('deletecustomer/<str:pk>/',views.deletecustomer,name='deletecustomer'),

     path('reset_password/',auth_views.PasswordResetView.as_view(template_name="CRM_app/password_reset.html"),
            name="reset_password"),

     path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="CRM_app/password_reset_set.html"),
            name="password_reset_done"),

     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="CRM_app/password_reset_form.html"),
            name="password_reset_confirm"),

     path('rest_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="CRM_app/password_reset_done.html"),
            name="password_reset_complete"),

]
