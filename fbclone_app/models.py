from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.contrib import admin

class Share(models.Model):
	content = models.CharField(max_length=1000)
	user = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now=True, blank=True)

class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'creation_date')

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	friends = models.ManyToManyField('self', related_name='friend_of', symmetrical=True)

	def gravatar_url(self):
		return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Share, ShareAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

