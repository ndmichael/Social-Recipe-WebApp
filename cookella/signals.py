"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FoodType
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


THUMBNAIL_SIZE = (200, 200)


@receiver(pre_save, sender=FoodType)
def generate_thumbnail(sender, instance, **kwargs):
    image = Image.open(instance.food_image)
    image = image.convert("RGB")
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()
    image.save(temp_thumb, "JPEG")
    temp_thumb.seek(0)


    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(
        instance.food_image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )
    temp_thumb.close()

"""
