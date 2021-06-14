from django.contrib import messages
from django.contrib.auth.models import Group

def add_to_group(request, queryset, group_name):
    group = Group.objects.get(name=group_name)
    for user in queryset:
        user.groups.add(group)

    len_ = len(queryset)
    if len_:
        messages.success(request,
            f'{len_} account(s) added to {group_name}.')

def remove_from_group(request, queryset, group_name):
    group = Group.objects.get(name=group_name)
    for user in queryset:
        user.groups.remove(group)

    len_ = len(queryset)
    if len_:
        messages.success(request,
            f'{len_} account(s) removed from {group_name}.')

def activate_account(request, queryset):
    queryset.update(is_active=True)
    len_ = len(queryset)
    if len_:
        messages.success(request,
            f'{len_} account(s) activated.')

def deactivate_account(request, queryset):
    superusers = queryset.filter(is_superuser=True)
    if superusers and not request.user.is_superuser:
        queryset = queryset.filter(is_superuser=False)
        usernames = ', '.join([user.username for user in superusers])
        messages.error(request,
            f"You don't have permission to deactivate {usernames}.")

    queryset.update(is_active=False)
    len_ = len(queryset)
    if len_:
        messages.success(request,
            f'{len_} account(s) deactivated.')
