from account.models import Account
from funding.models import Funding
from remit.models import Remit

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from rest_framework.exceptions import APIException, ValidationError

from .exceptions import JwtException, NoContentException

class Verify(JWTStatelessUserAuthentication):

    def jwt(self, request):
        print('start verify')
        if(request.headers.get("Authorization")):
            user = JWTStatelessUserAuthentication.authenticate(self, request=request)
            if(user):
                print(user)
                return user[0]
            else:
                raise JwtException(detail='unknown Token')
        else:
            raise JwtException(detail="NO ACCESS TOKEN")
            

    def account(request):
        print("start")
        if(request.GET.get('id')):
            try:
                account = Account.objects.get(id=request.GET.get('id'))
            except Account.DoesNotExist:
                raise NoContentException(detail="can't find user")
            return account
        elif(request.data.get('id')):
            try :
                account = Account.objects.get(id=request.data.get('id'))
            except Account.DoesNotExist:
                raise NoContentException(detail="can't find user")
            return account
        else:
            raise ValidationError(detail='bad request')

    

    def funding(request):
        if(request.GET.get('id')):
            try:
                funding = Funding.objects.get(id=request.GET.get('id'))
            except Funding.DoesNotExist:
                raise NoContentException(detail="can't find funding")
            return funding
        
        elif(request.data.get('id')):
            try :
                funding = Funding.objects.get(id=request.data.get('id'))
            except Funding.DoesNotExist:
                raise NoContentException(detail="can't find funding")
            return funding
        else:
            raise ValidationError(detail='bad request')
        
    
    def remit(request):
        if(request.GET.get('id')):
            try:
                remit = Remit.objects.get(id=request.GET.get('id'))
            except Remit.DoesNotExist:
                raise NoContentException(detail="can't find remit")
            return remit
        
        elif(request.data.get('id')):
            try :
                remit = Remit.objects.get(id=request.data.get('id'))
            except Remit.DoesNotExist:
                raise NoContentException(detail="can't find remit")
            return remit
        else:
            raise ValidationError(detail='bad request')