from account.models import Account
from funding.models import Funding
from remit.models import Remit

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from rest_framework.exceptions import ValidationError

from .exceptions import JwtException, NoContentException

#image upload
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

#paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class Verify(JWTStatelessUserAuthentication):

    def jwt(self, request):
        print('start verify')
        if(request.headers.get("Authorization")):
            user = JWTStatelessUserAuthentication.authenticate(self, request=request)
            if(user):
                print(user[0])
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
        

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def image_upload(id):
    path = 'profile_image/'
    return f'{path}{id}.png'

def funding_image_upload(id):
    path = 'funding_image/'
    return f'{path}{id}.png'


def review_image_upload(id):
    path = 'review_image/'
    return f'{path}{id}.png'



def paging_funding(request, list):

    page = request.GET.get('page')

    paginator = Paginator(list, 8)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        raise NoContentException(detail="no more content")

    return page_obj



def paging_remit(request, list):

    page = request.GET.get('page')

    paginator = Paginator(list, 8)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        raise NoContentException(detail="no more content")

    return page_obj