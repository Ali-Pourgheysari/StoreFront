from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255)

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # GenericType for product
    contect_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveBigIntegerField()
    content_object =  GenericForeignKey()