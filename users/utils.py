import jwt

from django.http import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def LoginStatus(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization', None)
            if token:
                payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user         = User.objects.get(id = payload['id'])
                request.user = user
            else:
                return JsonResponse({'result':'PLEASE LOGIN'}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'result' : 'INVALID TOKEN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'result' : 'TOKEN EXPIRED'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'result' : 'INVALID USER'}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper