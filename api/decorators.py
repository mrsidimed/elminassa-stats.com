from django.core.exceptions import PermissionDenied
import jwt
from django.conf import settings


def auth_required(function):
    def wrap(request, *args, **kwargs):
         

        tokenBearer = request.META.get('HTTP_AUTHORIZATION')
        print(tokenBearer)

        key  = settings.JWT_KEY
        resu = tokenBearer.split(" ")
        token = resu[1]

        print('token = '+ str(token))

        if not token: 
             raise PermissionDenied
    
        try:
            payload = jwt.decode(token , key , algorithms=['HS256'] )
            return function(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            raise PermissionDenied

        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap