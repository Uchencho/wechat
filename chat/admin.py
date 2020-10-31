from django.contrib import admin
from .models import Thread, ChatMessage

# Register your models here.
class ThreadAdmin(admin.ModelAdmin):

    model = Thread

    list_display = ['id', 'first', 'second', 'updated', 'timestamp']

class ChatAdmin(admin.ModelAdmin):
    model = ChatMessage
    list_display = ['id', 'thread', 'user', 'message', 'timestamp']

admin.site.register(Thread, ThreadAdmin)
admin.site.register(ChatMessage, ChatAdmin)
