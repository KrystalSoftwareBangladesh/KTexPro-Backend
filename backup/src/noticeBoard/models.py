from django.db import models

# Create your models here.
class notice(models.Model):
	title = models.CharField(max_length=120)
	image = models.