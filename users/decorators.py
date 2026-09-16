from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def mentor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_mentor or request.user.is_admin):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper