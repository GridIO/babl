from django.db import models
from core.models import User
import os
from django.db.models import Max

from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from images.storage import OverwriteStorage
from django.utils.translation import ugettext_lazy as _
import uuid

from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/user_<id>/<filename>
    return 'profile_images/user_%s/%s' % (instance.user.id, filename)


class Image(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to=user_directory_path_profile,
                              storage=OverwriteStorage())
    order = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def _save(self, *args, **kwargs):
        # compress image before saving
        if self.image:
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
                output, 'ImageField', "%s.jpg" % (self.uuid),
                'image/jpeg', output.seek(0, os.SEEK_END), None
            )

        # save normally
        super(Image, self).save()


class ProfileImage(Image):

    class Meta:
        verbose_name = _('Profile Image')
        verbose_name_plural = _('Profile Images')

    def __str__(self):
        return 'Propic #%s for user: %s' % (self.order, self.user.display_name)

    def save(self, *args, **kwargs):
        # check that user doesn't have 6 profile_images, raise error otherwise
        profile_imgs = ProfileImage.objects.filter(user=self.user)

        if len(profile_imgs) >= 6:
            raise RuntimeError("You may only have 6 profile images at a time.")
        else:
            order_max = profile_imgs.aggregate(Max('order'))['order__max']

            if order_max is None:
                self.order = 0
            else:
                self.order = order_max + 1

        self._save(self, *args, **kwargs)


@receiver(post_delete, sender=Image)
def profile_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
