from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils._os import safe_join

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
import os

from directmessages.exceptions import RecipientCantBeSelf
from directmessages.exceptions import ContentMustBeSpecified
from directmessages.exceptions import ContentCanOnlyBeSingleMedium
from directmessages.exceptions import ContentMustMatchIndicatedType

from core.models import Language
from google.cloud import translate
from google.oauth2 import service_account


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/message_images/user_<id>/user_<id>/<filename>
    return 'message_images/user_%s/user_%s/%s' % (instance.sender.id, instance.recipient.id, filename)


@python_2_unicode_compatible
class Message(models.Model):
    """
    A private translated directmessage
    """

    TYPE_CHOICES = (
        ('txt', 'Text'),
        ('img', 'Image'),
    )

    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='sent_dm',
        verbose_name=_("Sender"),
        db_index=True
    )
    recipient = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='received_dm',
        verbose_name=_("Recipient"),
        db_index=True
    )
    message_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES
    )
    sender_content = models.TextField(
        verbose_name=_('Content'),
        null=True,
        blank=True
    )
    recipient_content = models.TextField(
        verbose_name=_('Content (Translated)'),
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_('Image Content'),
        upload_to=user_directory_path_profile,
        null=True,
        blank=True
    )
    sender_language = models.ForeignKey(
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
    sent_at = models.DateTimeField(_("Sent At"), null=True, blank=True)
    read_at = models.DateTimeField(_("Read At"), null=True, blank=True)

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
        if self.message_type == 'txt':
            return self.sender_content
        elif self.message_type == 'img':
            return self.image.name

    def translate(self):
        """Translate original content to recipient's language"""

        # get credentials for google authentication
        credentials = service_account.Credentials.from_service_account_file(
            safe_join(settings.STATIC_ROOT, 'service-credentials.json')
        )

        # initialize client for translations
        client = translate.Client(credentials=credentials)

        # do translation
        self.recipient_content = client.translate(
            self.sender_content,
            target_language=self.recipient.language.lang_code,
            source_language=self.sender.language.lang_code
        )['translatedText']

        # note the languages assumed in the translation
        self.recipient_language = self.recipient.language
        self.sender_language = self.sender.language

    def clean(self):
        if self.sender == self.recipient:
            raise RecipientCantBeSelf

        # ensure content is uploaded
        if not self.sender_content and not self.image:
            raise ContentMustBeSpecified

        # prevent double uploads
        if self.sender_content and self.image:
            raise ContentCanOnlyBeSingleMedium

        # ensure that types match
        if self.sender_content and self.message_type != 'txt':
            raise ContentMustMatchIndicatedType

        if self.image and self.message_type != 'img':
            raise ContentMustMatchIndicatedType

    def save(self, **kwargs):
        self.full_clean()

        if not self.id:
            self.sent_at = timezone.now()

        # run translation
        if self.message_type == 'txt':

            if self.sender.language != self.recipient.language:
                self.translate()

            else:
                self.recipient_translated = self.sender_content

        elif self.message_type == 'img' and self.pk is None:
            self.sender_content = None

            img = Img.open(BytesIO(self.image.read()))

            if img.mode != 'RGB':
                img = img.convert('RGB')

            img.thumbnail(
                (self.image.width / 1.5, self.image.height / 1.5),
                Img.ANTIALIAS
            )
            output = BytesIO()

            img.save(output, format='JPEG', quality=25)
            self.image = InMemoryUploadedFile(
                output, 'ImageField', "%s.jpg" % uuid.uuid4(),
                'image/jpeg', output.seek(0, os.SEEK_END), None
            )

        super(Message, self).save(**kwargs)
