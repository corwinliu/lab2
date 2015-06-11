from django.db import models
from django.contrib.auth.models import User

MAX_CHAR_LENGTH = 200
MAX_FILE_LENGTH = 3500000



class PHOTO(models.Model):
	photo = models.ImageField(null=True,max_length=MAX_FILE_LENGTH,upload_to='photos/%Y/%m/%d')
	def image_tag(self):
		if self.photo:
			return u'<img src="%s" width="200px" height="200px" />' % self.photo.url
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True