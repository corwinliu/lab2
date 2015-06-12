from django.contrib import admin
from usermanager.models import *
# Register your models here.
class photoAdmin(admin.ModelAdmin):
	list_display = ('image_tag',)
	readonly_fields = ('image_tag',)
admin.site.register(PHOTO,photoAdmin)
admin.site.register(LOG)