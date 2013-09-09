from django.db import models
from django.contrib.auth.models import User
import hashlib

class Share(models.Model):
	content = models.Charfield(max_length=1000)
	user = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now=True, blank=True)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	friend = models.ManyToManyField('self', related_name='friend_of', symmetrical=True)

	def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Create your models here.
