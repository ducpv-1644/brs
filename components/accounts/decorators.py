from django.http import HttpResponseForbidden

from .models import Account


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            account = Account.objects.get(user=request.user)
            if account.role != '0':
                return HttpResponseForbidden('403 Forbidden')
            return function(request, *args, **kwargs)
        except:
            return HttpResponseForbidden('403 Forbidden')
    return wrapper
