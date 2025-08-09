from django.contrib import admin
from .models import lecture
# Register your models here.

class lectureAdmin(admin.ModelAdmin):
	class Meta:
		model = lecture

admin.site.register(lecture, lectureAdmin)