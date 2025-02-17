from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('profile/', views.profile, name="profile"),

    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgotpassword/', views.forgot_password_, name="forgot_password"),
    path('resetpasswordvalidate/<uidb64>/<token>', views.reset_password_validate, name="reset_password_validate"),
    path('resetpassword/', views.reset_password_, name="reset_password"),
    

]
