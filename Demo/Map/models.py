from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=156, unique=True)
    slug = models.SlugField(max_length=156, blank=True, unique=True)

    def save(self, *args, **kwargs):#adminde save_model models de save
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=156,  unique=True)
    slug = models.SlugField(max_length=156, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=156)
    qx = models.FloatField()
    qy = models.FloatField()
    is_metropolitan = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    slug = models.SlugField(max_length=156, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.name}-{self.country}"


class CityCSVUpload(models.Model):
    root_storage = FileSystemStorage(location=settings.BASE_DIR)
    file = models.FileField(storage=root_storage, upload_to="csv/")  # → BASE_DIR/csv/<dosya>
    def __str__(self):
        return self.file.name