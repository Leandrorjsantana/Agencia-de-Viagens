# subscribers/admin.py

from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

    def has_add_permission(self, request):
        # Impede a adição manual de e-mails pelo admin
        return False