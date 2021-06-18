from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()

@register.filter
def get_option_text(question, option):
    if option == 'A':
        return question.option_A
    elif option == 'B':
        return question.option_B
    elif option == 'C':
        return question.option_C
    elif option == 'D':
        return question.option_D
