from django.db import models
from django.conf import settings
import os
from django.db.models import Max

from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from images.storage import OverwriteStorage
from django.utils.translation import ugettext_lazy as _
import uuid

from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch.dispatcher import receiver

from django.core.exceptions import ObjectDoesNotExist
from images.exceptions import TooManyImages
from images.exceptions import DuplicateImage
from images.exceptions import ImageNotAvailable
from images.exceptions import NextImageCannotBeSelf

from django.contrib.auth import get_user_model

# HELPER FUNCTIONS

User = get_user_model()


def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/user_<id>/<filename>
    return 'profile_images/user_%s/%s' % (instance.user.id, filename)


def get_images(image, depth=settings.PROFILE_IMAGE_LIMIT):
    """
    Creates list of images ordered using next_image

    :param image: instance of ProfileImage
    :param depth: depth, must be <= settings.PROFILE_IMAGE_LIMIT
    :return: list of images ordered according to their order
    """
    images = []

    def recurse(_image, _depth):

        # add image to the parent list
        images.append(_image)

        # if desired recursive depth is reached or the next image is null
        if _depth == 0 or not _image.next_image:
            return None

        else:
            recurse(_image.next_image, _depth-1)

    recurse(image, depth)

    return images


def get_last_2(images_list):
    """
    Retrieve last two images from a list and returns a tuple.
    If list passed has the settings.PROFILE_IMAGE_LIMIT number of elements,
    then return the last element and None in a tuple.

    :param images_list: a list of ProfileImage instances ordered accordingly
    :return: tuple containing either two ProfileImage instances or one instance + None
    """
    if len(images_list) < settings.PROFILE_IMAGE_LIMIT:
        return images_list[-2:]

    return [images_list[-1], None]


# MODELS


class ProfileImage(models.Model):

    STATUS_CHOICES = (
        ('PEN', 'Pending'),
        ('APP', 'Approved'),
        ('REJ', 'Rejected')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, related_name='images',
                             verbose_name=_('User'))
    image = models.ImageField(upload_to=user_directory_path_profile,
                              storage=OverwriteStorage(), verbose_name=_('Image File'))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES,
                              default='PEN', verbose_name=_('Status'))
    primary = models.BooleanField(default=False, verbose_name=_('Primary Image'))
    next_image = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL,
                                   verbose_name=_('Next Image'))

    class Meta:
        verbose_name = _('Profile Image')
        verbose_name_plural = _('Profile Images')

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        # check that user doesn't have allowed number of profile_images, raise error otherwise
        if len(ProfileImage.objects.filter(user=self.user)) > settings.PROFILE_IMAGE_LIMIT:
            raise TooManyImages

        # check that next image is not self
        if self.next_image == self:
            raise NextImageCannotBeSelf

        # compress image before saving
        if self.image and self.pk is None:
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
                output, 'ImageField', "%s.jpg" % self.uuid,
                'image/jpeg', output.seek(0, os.SEEK_END), None
            )

        # save
        super(ProfileImage, self).save()

    def move(self, index, *args, **kwargs):
        """
        Move image to index within user profile images.

        Added per issue #18.

        :param index: define location for move, must be integer
        :return: None

        Glossary:
        - pre_operation_primary = the image that is the primary for user before any operations are performed
        - pre_operation_previous = the image preceding self before any operations are performed
        - pre_operation_next = the image that comes after self before any operations are performed
        - post_operation_previous = the image preceding self after desired operations are performed
        - post_operation_next = the image that comes after self after any desired operations are performed
        """
        if len(ProfileImage.objects.filter(user=self.user)) < 2:
            return self  # do nothing, since there's nowhere else to move

        if index == 0:
            if self.primary:

                print('index 0, primary true')

                return self  # do nothing, since this would move it to the same place

            else:

                print('index 0, primary false')

                # Find `pre_operation_previous`
                pre_operation_previous = ProfileImage.objects.get(next_image=self)

                # Find `pre_operation_next`
                pre_operation_next = self.next_image

                # Make `pre_operation_previous.next_image = pre_operation_next`
                pre_operation_previous.next_image = pre_operation_next

                # Done with `pre_operation_previous` -- save
                pre_operation_previous.save()

                # Find `pre_operation_primary`
                pre_operation_primary = ProfileImage.objects.get(primary=True, user=self.user)

                # Make `pre_operation_primary.primary = False`
                pre_operation_primary.primary = False

                # Make `self.primary = True`
                self.primary = True

                # Make `self.next_image = pre_operation_primary`
                self.next_image = pre_operation_primary

                # Done with `self` and `pre_operation_primary` -- save both
                pre_operation_primary.save()
                self.save()

                return self

        else:
            if self.primary:

                print('index >0, primary true')

                # Find `pre_operation_next`
                pre_operation_next = self.next_image

                # Make `self.primary = False`
                self.primary = False

                # Make `pre_operation_next.primary = True`
                pre_operation_next.primary = True

                # Done with `pre_operation_next` -- save
                pre_operation_next.save()

                # Need to update db with current self -- save
                self.save()

                # Get last two images through to index+1 as `post_operation_previous`
                # and `post_operation_next`, respectively
                image_list = get_images(
                    ProfileImage.objects.get(primary=True, user=self.user),
                    depth=index
                )
                post_operation_previous, post_operation_next = get_last_2(image_list)

                # Make `post_operation_previous.next_image = self`
                post_operation_previous.next_image = self

                # Make `self.next_image = post_operation_next`
                self.next_image = post_operation_next

                # Done with `self` and `post_operation_previous` -- save both
                post_operation_previous.save()
                self.save()

                return self

            else:

                print('index >0, primary false')

                # Find `pre_operation_previous`
                pre_operation_previous = ProfileImage.objects.get(next_image=self)

                # Find `pre_operation_next`
                pre_operation_next = self.next_image

                # Make `pre_operation_previous.next_image = pre_operation_next`
                pre_operation_previous.next_image = pre_operation_next

                # Done with `pre_operation_previous` -- save
                pre_operation_previous.save()

                # Get last two images through to index+1 as `post_operation_previous`
                # and `post_operation_next`, respectively
                image_list = get_images(
                    ProfileImage.objects.get(primary=True, user=self.user),
                    depth=index
                )
                post_operation_previous, post_operation_next = get_last_2(image_list)

                # Make `post_operation_previous.next_image = self`
                post_operation_previous.next_image = self

                # Make `self.next_image = post_operation_next`
                self.next_image = post_operation_next

                # Done with `self` and `post_operation_previous` -- save both
                post_operation_previous.save()
                self.save()

                return self


# SIGNALS

@receiver(post_save, sender=ProfileImage)
def profile_image_post_save(sender, instance, created, **kwargs):
    """
    Updated per issue #18
    """
    if created:
        images = sender.objects.filter(user=instance.user).exclude(id=instance.id)

        if len(images) == 0:
            instance.primary = True
            instance.save()

        else:
            previous = images.get(next_image__isnull=True)
            previous.next_image = instance
            previous.save()

    else:
        # delete object if rejected
        if instance.status == 'REJ':
            instance.delete()

        # TODO: send user an email informing them that their profile image was rejected


@receiver(pre_delete, sender=ProfileImage)
def profile_image_pre_delete(sender, instance, **kwargs):
    """
    Created per issue #18
    """
    if instance.primary:
        next_img = instance.next_image
        next_img.primary = True
        next_img.save()

    else:
        if instance.next_image:
            next_img = instance.next_image
            previous = ProfileImage.objects.get(next_image=instance)
            previous.next_image = next_img
            previous.save()

        else:
            pass  # nothing needs to be done


@receiver(post_delete, sender=ProfileImage)
def profile_image_post_delete(sender, instance, **kwargs):
    """
    Updated per issue #18
    """
    # delete actual image file
    instance.image.delete(False)

