import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.http    import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers["Authorization"]
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload["id"])
            request.user = user

        except KeyError:
            return JsonResponse({"message":"NO_TOKEN"}, status=400)

        except DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        except ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
