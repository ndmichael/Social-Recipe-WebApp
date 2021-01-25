from django.db import models
from django.contrib.auth.admin import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.TextField(max_length=200, default='No profile details set yet by the user')
    image = models.ImageField(default='avatar.png', upload_to='profile_pics/', blank=True, null=True)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/avatar.png"
    """
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 600 and img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path) """

    def __str__(self):
        return f'{self.user.username} Profile'



