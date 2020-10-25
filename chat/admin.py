from django.contrib import admin
from .models import Thread

# Register your models here.
class ThreadAdmin(admin.ModelAdmin):

    model = Thread

    list_display = ['id', 'first', 'second', 'updated', 'timestamp']

admin.site.register(Thread, ThreadAdmin)
