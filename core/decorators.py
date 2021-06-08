from django.core.exceptions import PermissionDenied

def group_required(group_name):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if (request.user.groups.filter(name=group_name).exists() or
                    request.user.is_superuser):
                return view(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapper

    return decorator
