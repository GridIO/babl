from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static

from core.models import Language
from google.cloud import translate
from google.oauth2 import service_account


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Message(models.Model):
    """
    A private translated directmessage
    """
    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='sent_dm',
        verbose_name=_("Sender")
    )
    recipient = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='received_dm',
        verbose_name=_("Recipient")
    )
    content = models.TextField(_('Content'))
    content_translated = models.TextField(
        _('Content (Translated)'),
        null=True,
        blank=True
    )
    source_language = models.ForeignKey(
        Language,
        null=True,
        blank=True,
        related_name='source_language',
        verbose_name=_('Source Language')
    )
    recipient_language = models.ForeignKey(
        Language,
        null=True,
        blank=True,
        related_name='recipient_language',
        verbose_name=_('Recipient Language')
    )
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    @property
    def unread(self):
        """return whether the message was read or not"""
        if self.read_at is not None:
            return False
        return True

    def __str__(self):
        return self.content

    def translate(self):
        """Translate original content to recipient's language"""

        # get credentials for google authentication
        credentials = service_account.Credentials.from_service_account_file(
            settings.BASE_DIR + static('service-credentials.json')
        )

        # initialize client for translations
        client = translate.Client(credentials=credentials)

        # do translation
        self.content_translated = client.translate(
            self.content,
            target_language=self.recipient.language.lang_code,
            source_language=self.sender.language.lang_code
        )['translatedText']

        # note the languages assumed in the translation
        self.recipient_language = self.recipient.language
        self.source_language = self.sender.language

    def save(self, **kwargs):
        if self.sender == self.recipient:
            raise ValidationError("You can't send messages to yourself")

        if not self.id:
            self.sent_at = timezone.now()

        # run translation
        if self.content_translated is None or self.content_translated == '':
            self.translate()

        super(Message, self).save(**kwargs)
