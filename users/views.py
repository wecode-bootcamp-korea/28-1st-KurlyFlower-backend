import json
import re
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from json.decoder           import JSONDecodeError
from datetime               import datetime, timedelta
from my_settings            import SECRET_KEY, ALGORITHM

def validate_username(username):
    REGEX_USERNAME = '^(?=.*[a-zA-Z])[a-zA-Z0-9]{6,}$'

    if not re.match(REGEX_USERNAME,username):
        raise ValidationError('USERNAME_VALIDATION')

def validate_password(password):
    REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

    if not re.match(REGEX_PASSWORD,password):
        raise ValidationError('PASSWORD_VALIDATION')

def validate_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(REGEX_EMAIL,email):
        raise ValidationError('EMAIL_VALIDATION')

class SignupView(View):
    def post(self,request):

        try:
            data = json.loads(request.body)

            if User.objects.filter(username = data['username']).exists():
                return JsonResponse({'message' : 'USERNAME_DUPLICATE_VALUES'}, status = 400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'EMAIL_DUPLICATE_VALUES'}, status = 400)

            validate_username(data['username'])
            validate_password(data['password'])
            validate_email(data['email'])

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                username     = data['username'],
                password     = hashed_password.decode('utf-8'),
                name         = data['name'],
                email        = data['email'],
                phone_number = data['phone_number'],
                address      = data['address']
            )
            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSONDECODE_ERROR'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message' : e.messages}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data["username"]
            password = data["password"].encode("utf-8")

            user = User.objects.get(username=username)

            if not bcrypt.checkpw(password, user.password.encode("utf-8")):
                raise ValidationError

            payload = {
                "id"  : user.id,
                "exp" : datetime.now()+timedelta(days=7),
                "iat" : datetime.now()
            }
            access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
            return JsonResponse({"access_token": access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message":"INVALID_JSON"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)

        except ValidationError:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
