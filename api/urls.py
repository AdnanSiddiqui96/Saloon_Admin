from django.urls import path,include
from api.views import *

urlpatterns = [

#web urls  home
path('AdminLogin',AdminLogin.as_view()),
path('superadmindminLogin',SuperAdminLogin.as_view()),
path('AdminRegister',AdminRegister.as_view()),
path('Salons',Salons.as_view()),
path('catagory',Catagory.as_view()),
path('Survices',Survices.as_view()),
# path('roles',roles.as_view()),
# path('dataget_saloon',dataget_saloon.as_view()),
# path('datagets',datagets.as_view()),
# path('dataget_survice',dataget_survice.as_view()),
# path('Employees',Employees.as_view()),
# path('Otp_sending',Otp_sending.as_view()),
# path('verify_otpcode',verify_otpcode.as_view()),
# path('Showsaloon',Showsaloon.as_view()),
# path('dataget_saloon',dataget_saloon.as_view()),
# path('Salon_Sub_detail',Salon_Sub_detail.as_view()),
# path('search',search.as_view()),
# path('addimages',addimages.as_view()),
# path('float_list_data',float_list_data.as_view()),
# path('dataget_image',dataget_image.as_view()),


]