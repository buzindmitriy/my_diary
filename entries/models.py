from django.db import models
from django.conf import settings
from django.utils.text import slugify
import markdown

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Entry(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField('Содержание')
    html_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='entry_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.html_content = markdown.markdown(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
