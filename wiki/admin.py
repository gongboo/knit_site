from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import WikiPost

admin.site.register(WikiPost, SimpleHistoryAdmin)