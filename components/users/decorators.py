from django.http import HttpResponseForbidden


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.role != 1:
                return HttpResponseForbidden('403 Forbidden')
            return function(request, *args, **kwargs)
        except:
            return HttpResponseForbidden('403 Forbidden')
    return wrapper
