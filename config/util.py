from account.models import Account
from funding.models import Funding
from remit.models import Remit
from django.http import response


class Verify():
    def account(request):
        if(request.GET.get('id')):
            try:
                account = Account.objects.get(id=request.GET.get('id'))
            except Account.DoesNotExist:
                return response.HttpResponse(status=410)
            return account
        
        elif(request.data.get('id')):
            try :
                account = Account.objects.get(id=request.data.get('id'))
            except Account.DoesNotExist:
                return response.HttpResponse(status=410)
            return account
        else:
            return response.HttpResponse(status=404)


    def author(request):
        try:
            author = Account.objects.get(id=request.data.get('author'))
        except Account.DoesNotExist:
            return response.HttpResponse(status=410)
        except:
            return response.HttpResponse(status=404)
        
        return author
    

    def funding(request):
        if(request.GET.get('id')):
            try:
                funding = Funding.objects.get(id=request.GET.get('id'))
            except Funding.DoesNotExist:
                return response.HttpResponse(status=420)
            return funding
        
        elif(request.data.get('id')):
            try :
                funding = Funding.objects.get(id=request.data.get('id'))
            except Funding.DoesNotExist:
                return response.HttpResponse(status=420)
            return funding
        else:
            return response.HttpResponse(status=404)
        
    
    def remit(request):
        if(request.GET.get('id')):
            try:
                remit = Remit.objects.get(id=request.GET.get('id'))
            except Remit.DoesNotExist:
                return response.HttpResponse(status=420)
            return remit
        
        elif(request.data.get('id')):
            try :
                remit = Remit.objects.get(id=request.data.get('id'))
            except Remit.DoesNotExist:
                return response.HttpResponse(status=420)
            return remit
        else:
            return response.HttpResponse(status=404)