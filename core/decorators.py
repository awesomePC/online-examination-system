from django.core.exceptions import PermissionDenied


def group_required(*group_names):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if (
                request.user.groups.filter(name__in=group_names).exists()
                or request.user.is_superuser
            ):
                return view(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapper

    return decorator


def is_verified_student(view):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, "student"):
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper


def is_verified_teacher(view):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, "teacher"):
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper


def is_hod(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_hod:
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper
