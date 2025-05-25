from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL, verbose_name="Parent Category")
    status = models.BooleanField(default=True, verbose_name="Status")
    image = models.ImageField(upload_to='category_pics/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            # Convert name to lowercase with underscores
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.timestamp}'

    