from .models import Message
from django.contrib import admin


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'recipient', 'content', 'content_translated',)

    class Meta:
        fields = (
            'sender', 'recipient', 'content', 'content_translated',
            'source_language', 'recipient_language', 'sent_at', 'read_at',
        )


admin.site.register(Message, MessageAdmin)
