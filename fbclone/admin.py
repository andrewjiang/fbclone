from django.contrib import admin
from fbclone.fbclone_app.models import Share, UserProfile

class ShareAdmin(admin.ModelAdmin):
	pass
admin.site.register(Share, ShareAdmin)