# company_info/admin.py
from django.contrib import admin
from .models import TeamMember
from adminsortable2.admin import SortableAdminMixin

@admin.register(TeamMember)
class TeamMemberAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'role')