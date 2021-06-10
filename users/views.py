from users.utils import LoginStatus
from django.shortcuts import render

# Create your views here.
import json, re, bcrypt, jwt

from django.db.models.fields.json import DataContains

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from users.models import User
from my_settings import ALGORITHM, SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            name         = data['name']
            password     = data['password']
            sex          = data['sex']
            admin        = data['admin']

            PHONE_NUMBER_REGEX  = "^[0-9]{10,11}$"
            PASSWORD_REGEX      = "(?=.*\d)(?=.*[a-z]).{5,}"
            NAME_REGEX          = "^[가-힣a-zA-Z ]+$"

            if not re.search(PHONE_NUMBER_REGEX, phone_number):
                return JsonResponse({'result' : 'VALIDATION ERROR : INVALID PHONE NUMBER'}, status=400)
            if not re.search(PASSWORD_REGEX, password):
                return JsonResponse({'result' : 'VALIDATION ERROR : INVALID PASSWORD'}, status=400)
            if not re.search(NAME_REGEX, name):
                return JsonResponse({'result' : 'VALIDATION ERROR : INVALID USERNAME'}, status = 400)   
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'result' : 'PHONE NUMBER ALREADY EXISTS'})

            hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                phone_number = phone_number,
                password     = hashed_password.decode('utf-8'),
                name         = name,
                sex          = sex,
                admin        = admin,
            )
            return JsonResponse({'result' : 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'result' : 'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            phone_number = data['phone_number']
            password     = data['password']

            if not User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'result' : 'INVALID USER'}, status=401)

            user_data=User.objects.get(phone_number=phone_number)

            if not bcrypt.checkpw(password.encode('utf-8'), user_data.password.encode('utf-8')):
                return JsonResponse({'result' : 'INVALID PASSWORD'}, status=401)

            token=jwt.encode({'phone_number' : phone_number}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'result' : 'SUCCESS!', 'token' : token}, status=201)

        except KeyError:
            return JsonResponse({'result' : 'KEY_ERROR'}, status=400)
        

