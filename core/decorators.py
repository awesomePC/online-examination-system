from django.core.exceptions import PermissionDenied

def group_required(*group_names):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if (request.user.groups.filter(name__in=group_names).exists() or
                    request.user.is_superuser):
                return view(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapper

    return decorator

def group_forbidden(*group_names):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if (request.user.groups.filter(name__in=group_names).exists() and
                    not request.user.is_superuser):
                raise PermissionDenied()
            else:
                return view(request, *args, **kwargs)

        return wrapper

    return decorator
