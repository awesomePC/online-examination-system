from django.contrib import admin
from .models import Exam, Session

class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'duration',
        'get_num_questions',
        'get_max_marks',
        'passing_percentage',
        'active',
        'created',
    )
    list_filter = ('active', 'created')
    search_fields = ('name', 'user__username')


class SessionAdmin(admin.ModelAdmin):
    exclude = ('bookmarks',)
    list_display = (
        'exam',
        'user',
        'completed',
        'get_marks',
        'get_max_marks',
        'get_num_attempted_que',
        'get_num_total_que',
        'get_passing_status',
        'created',
        'submitted',
    )
    list_filter = ('completed', 'created', 'submitted')
    search_fields = ('exam__name', 'user__username')


admin.site.register(Exam, ExamAdmin)
admin.site.register(Session, SessionAdmin)
