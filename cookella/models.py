from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.text import slugify
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.urls import reverse


from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category model implemented with mptt
    """

    name = models.CharField(
        verbose_name="Recipe Category",
        help_text="Required and Unique",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(
        self, *args, **kwargs
    ):  # i override the save method to prepopulate slugs, another way is using signals
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_list", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class FoodType(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="food_category"
    )
    contributor = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="contributor"
    )
    food_name = models.CharField(max_length=50, null=False)
    country = CountryField(
        blank_label="(select a country)",
    )
    slug = models.SlugField(max_length=100, unique_for_date="date_added")
    active = models.BooleanField(default=True)
    upvote = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)

    def save(
        self, *args, **kwargs
    ):  # i override the save to pre-populate slugs, another way is using signals
        self.slug = slugify(self.food_name)
        super(FoodType, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_name}"

    def get_absolute_url(self):
        return reverse("recipes", kwargs={"pk": self.pk, "slug": self.slug})

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
    food_type = models.OneToOneField(
        FoodType,
        on_delete=models.CASCADE,
        related_name="food_type",
        primary_key=True,
        unique=True,
    )
    ingredient = models.TextField()
    note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.recipe}"


class FoodImage(models.Model):
    food = models.ForeignKey(
        FoodType,
        on_delete=models.CASCADE,
        related_name="food_images",
    )
    images = models.ImageField(
        upload_to="food_photos/%Y/%m/%d", default="default.jpg", blank=False, null=False
    )
    is_feature = models.BooleanField(default=False)
