from .models import Message
from django.contrib import admin


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = (
        'sender', 'recipient', 'sender_content', 'recipient_content',
    )

    class Meta:
        fields = (
            'sender', 'recipient', 'sender_content', 'recipient_content',
            'sender_language', 'recipient_language', 'sent_at', 'read_at',
        )


admin.site.register(Message, MessageAdmin)
