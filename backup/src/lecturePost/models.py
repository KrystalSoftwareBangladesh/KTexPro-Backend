from django.db import models

# Create your models here.
class lecture(models.Model):
	courseName = models.CharField(default='Software Engineering', max_length=120)
	courseCode = models.IntegerField(default='321')
	description = models.TextField(default='Class lecture')
	date = models.DateField(auto_now=True, auto_now_add=False)
	lectureNo = models.IntegerField(null=False)
	downloadLink = models.URLField(null=False)
	time = models.TimeField()
	def __unicode__(self):
		return self.name
