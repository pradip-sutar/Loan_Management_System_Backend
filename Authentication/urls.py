from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('googleauth/login/', views.GoogleLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create-user/', views.CreateUserView.as_view(), name='create_user'),  # API endpoint for creating a user
    path('send-email/', views.send_email, name='send-email'),
    #path('users-listview/', views.UserListView.as_view(), name='user_list'),  # New endpoint for paginated user list
    path('send-otp/', views.send_verification_email, name='send_otp'), # New endpoint for
    path('otp-verify/', views.verify_email_otp, name='verify_email_otp'), # New endpoint for
    path('reset-password/', views.reset_admin_password, name='reset_admin_password'),

]
