from django.contrib import admin

from .models import (DataTwitter, Tweet, Keyword)

admin.site.register(DataTwitter)
admin.site.register(Tweet)
admin.site.register(Keyword)
