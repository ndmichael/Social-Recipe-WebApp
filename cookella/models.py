from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.text import slugify
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.urls import reverse

# Create your models here.


# Created Category which i think i might use for the future
class FoodType(models.Model):
    Categories = (
        ('Bakery', 'Bakery'),
        ('Dinner', 'Dinner'),
        ('BreakFast', 'BreakFast'),
        ('Events', 'Events'),
        ('Get together', 'Get together'),
    )
    food_name = models.CharField(max_length=50, null=False)
    country = CountryField(blank_label="(select a country)",)
    food_image = models.ImageField(upload_to='food_photos', default='default.jpg', )
    slug = models.SlugField(max_length=100, unique_for_date='date_added')
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    contributor = models.CharField(max_length=150, default='admin')

    def save(self, *args, **kwargs):  # i override the save to pre-populate slugs, another way is using signals
        self.slug = slugify(self.food_name)
        super(FoodType, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_name}"

    def get_absolute_url(self):
       return reverse('recipes', kwargs={'pk': self.pk, 'slug': self.slug})

    # resizes images to 400,400, commented out due to error on s3
    """def save(self):
        super().save()
        img = Image.open(self.food_image.path)
        if img.height > 400 or img.width > 400:
            new_size = (400, 400)
            img.thumbnail(new_size)
            img.save(self.food_image.path)
    """


class FoodRecipe(models.Model):
    recipe = models.TextField()
    food_type = models.OneToOneField(FoodType, on_delete=models.CASCADE, related_name='food_type', primary_key=True, unique=True)
    ingredient = models.TextField(max_length=1000)
    upvote = models.IntegerField(default=0)
    note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.recipe}"



