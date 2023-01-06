from django.shortcuts import render
# Create your views here.
import datetime
import jwt
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import generics
from .serializer import* 
# import saloon_admin.usable as uc
from .models import *              
import random

# saloon_web_adminsite

class dataget_saloon(APIView):
      def get(self,request):
          my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
          if my_token:

            data = saloon.objects.all().values('saloon_name','contact', CityName=F('city_id__name'), RoleName=F('role_id__role')).first()

            if data:
                return Response({'status': True,  'data': data})
            else:
                return Response({"status": False, "msg":"Invalid_Credentials"})
          else:
            return Response({"status": False, "msg":"Unauthorized"})

# Admin Register

class AdminRegister(APIView):
   def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            contact = request.data.get('contact')
            role_id = request.data.get('role_id')

            objrole = Role.objects.filter(role = 'admin').first()

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                checkemail=Account.objects.filter(email=email).first()
                if checkemail:
                    return Response({"status":False, "message":"Email already exists"})

                checkphone=Account.objects.filter(contact=contact).first()
                if checkphone:
                    return Response({"status":False, "message":"phone no already existsplease try different number"})

                data = Account(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact, role_id=objrole)

                data.save()

                return Response({"status":True,"message":"Account Created Successfully"})
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"})



# Admin Login
class AdminLogin(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)

         if validator:
            return Response(validator,status = 200)

         else:
               email = request.data.get('email')
               password = request.data.get('password')
               fetchAccount = Account.objects.filter(email=email).first()
               if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                    if fetchAccount.role_id.role == 'admin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname,
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                              'iat': datetime.datetime.utcnow(),
                           }


                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})
                    else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
               else:
                  return Response({"status":False,"message":"Unable to login"})

# CATAGORY-POST/API
#Bulk Insertion
class Catagory(APIView):
    def post(self, request):
        print(request.data)

        catlist = list()
        for i in request.data:
            saloonObj = saloon.objects.filter(uid= i['saloon_id_id']).first()
            catlist.append(category(category_name=i['category_name'],saloon_id=saloonObj))                       
        category.objects.bulk_create(catlist)                 
        return Response(request.data) 

    def get(self, request):
        data = category.objects.values()
        return Response({'status':True, 'data': data})
    
    def put(self, request):
        my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid','saloon_name','contact','city_id','service_id','image']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                category_name = request.data.get("category_name")
                saloon_id = request.data.get("saloon_id_id")               

                data = saloon.objects.filter(uid=uid).first()
                if data:
                    data.category_name=category_name
                    data.saloon_id=saloon_id                   
                    data.save()
                    return Response({'status': True, 'Msg': 'Saloon Updated Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})


    def delete(self,request):
        # my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
        # if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.GET['uid']
                data = category.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"ID not found."})
    #
        # else:
        #     return Response({"status": False, "msg":"Unauthorized"})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SALOON-POST/API

class Salons(APIView):
    def post(self, request):
            requireFields = ['saloon_name','contact','address','service_id','image']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator,status = 200)
            else:
                superadmin = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                admin = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
                if superadmin or admin:
                    saloon_name  = request.data.get('saloon_name')
                    contact  = request.data.get('contact')
                    address  = request.data.get('address')
                    city_id  = request.data.get('city_id')
                    service_id  = request.data.get('service_id')
                    image = request.data.getlist('image')

                    objcity = city.objects.filter(name = city_id).first()
                    objser = service.objects.filter(service_name = service_id).first()

                    checkphone=saloon.objects.filter(contact=contact).first()
                    if checkphone:
                        return Response({"status" : False, "message":"Contact number already exists please try different number"})
                    data = saloon(saloon_name=saloon_name,contact=contact,address=address ,service_id=objser , city_id=objcity)
                    data.save()
                    for i in range(len(image)):
                        pic = saloon_image(image=image[i],saloon_id =data)
                        pic.save()
                    return Response ({"status":True,"message":"Successfully Add"})
                else:
                    return Response({"status": False, "msg":"Unauthorized"})
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SALOON-GET/API

    def get(self, request):
        my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            # data = saloon.objects.all().values('saloon_name','contact', Employee_Information=F('Employee_Detail__name'), CityName=F('city_id__name'), RoleName=F('role_id__role'))
            data = saloon.objects.all().values('saloon_name','contact', cityName=F('city_id__name'),serviceName=F('service_id__service_name'))

            # data = saloon.objects.all().values()#service_id

            return Response({'status':True, 'data': data})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

####################################################################################################################
# SALOON-PUT/API
    # def put(self, request):
    #     my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
    #     if my_token:
    #         requireFields = ['uid','saloon_name','contact','city_id','service_id','image']
    #         validator = uc.keyValidation(True,True,request.data,requireFields)

    #         if validator:
    #             return Response(validator,status = 200)

    #         else:    
    #             uid = request.data.get('uid')
    #             saloon_name = request.data.get("saloon_name")
    #             contact = request.data.get("contact")
    #             address = request.data.get("address")
    #             city_id = request.data.get("city_id")
    #             service_id  = request.data.get('service_id')
    #             image = request.data.getlist('image')

            
    #             objcity = city.objects.filter(name = city_id).first()
    #             objser = service.objects.filter(service_name = service_id).first()

    #             admin = saloon.objects.filter(uid=uid).first()
    #             if admin:
    #                 admin.saloon_name=saloon_name
    #                 admin.contact=contact
    #                 admin.address=address
    #                 admin.city_id=objcity
    #                 admin.service_id=objser
    #                 admin.image=image

    #                 admin.save()

    #                 return Response({'status': True, 'Msg': 'data Update Successfully'}) 
    #             else:
    #                 return Response({"status": False, "msg":"invalid_Credentials"})
    #     else:
    #         return Response({"status": False, "msg":"Unauthorized"})    


    def put(self, request):
        my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid','saloon_name','contact','city_id','service_id','image']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                saloon_name = request.data.get("saloon_name")
                contact = request.data.get("contact")
                address = request.data.get("address")
                city_id = request.data.get("city_id")
                service_id  = request.data.get('service_id')
                image = request.data.getlist('image')

                objcity = city.objects.filter(name = city_id).first()
                objser = service.objects.filter(service_name = service_id).first()

                data = saloon.objects.filter(uid=uid).first()
                if data:
                    data.saloon_name=saloon_name
                    data.contact=contact
                    data.address=address
                    data.city_id=objcity
                    data.service_id=objser
                    data.image=image

                    data.save()

                    return Response({'status': True, 'Msg': 'Saloon Updated Successfully'})

                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})
####################################################################################################################################################
# SALOON-DELETE/API

    def delete(self,request):
        my_token = uc.admin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.GET['uid']
                data = saloon.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#
        else:
            return Response({"status": False, "msg":"Unauthorized"})


# SURVICE-POST/API
class Survices(APIView):
    def post(self, request):
            requireFields = ['service_name','description','price','image','Service_Date','Service_time','service_type']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator,status = 200)
            else:
                # my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                # if my_token:
                    service_name  = request.data.get('service_name')
                    description  = request.data.get('description')
                    price  = request.data.get('price')                    
                    image  = request.data.get('image')                    
                    Service_Date  = request.data.get('Service_Date')
                    Service_time = request.data.get('Service_time')
                    service_type = request.data.get('service_type')                                       
                    data = service(service_name=service_name,description=description,price=price,image=image,Service_Timing=Service_Date,before_time=Service_time,service_type=service_type )                    
                    data.save()
                    return Response ({"status":True,"message":"Successfully Add"})
                # else:
                #     return Response({"status": False, "msg":"Unauthorized"})          
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SURVICE-GET/API
    
    def get(self, request):
        # my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        # if my_token:
            # data = service.objects.all().values('description','price', Saloon_Name=F('saloon_id__saloon_name'), Added_By=F('Added_by__role'))
            data = service.objects.all().values()
                
            return Response({'status':True, 'data': data})       
        # else:
        #     return Response({"status": False, "msg":"Unauthorized"})  

####################################################################################################################  
# SURVICE-PUT/API
 
    def put(self, request):
        # my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        # if my_token:
            requireFields = ['uid', 'service_name','description','price','image','Service_Timing','before_time','service_type']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                uid = request.data.get('uid')       
                service_name  = request.data.get('service_name')
                description  = request.data.get('description')
                price  = request.data.get('price')                    
                image  = request.data.get('image')                    
                Service_Timing  = request.data.get('Service_Timing')
                before_time = request.data.get('before_time')
                service_type = request.data.get('service_type')                                      

                admin = service.objects.filter(uid=uid).first()
                if admin:
                    admin.service_name = service_name
                    admin.description = description
                    admin.price = price
                    admin.image = image
                    admin.Service_Timing = Service_Timing
                    admin.before_time = before_time
                    admin.service_type = service_type

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'}) 
                    
                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        # else:
        #     return Response({"status": False, "msg":"Unauthorized"})    
####################################################################################################################################################
# SURVICE-DELETE/API

    def delete(self,request):
        # my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        # if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)
 
            if validator:
                return Response(validator,status = 200)   

            else:
                uid = request.GET['uid']
                data = service.objects.filter(uid=uid).first()       
                if data:
                    data.delete()
                    
                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#     
        # else:
        #     return Response({"status": False, "msg":"Unauthorized"})

# SuperAdmin Login
class SuperAdminLogin(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)

         if validator:
            return Response(validator,status = 200)

         else:
               email = request.data.get('email')
               password = request.data.get('password')
               fetchAccount = Account.objects.filter(email=email).first()
               if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                    if fetchAccount.role_id.role == 'superadmin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname,
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                              'iat': datetime.datetime.utcnow(),
                           }
                        access_token = jwt.encode(access_token_payload,config('superadminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})
                    else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
               else:
                  return Response({"status":False,"message":"Unable to login"})
