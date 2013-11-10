from django.contrib import admin
from stories.models import Story



class StoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'domain', 'moderator', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    
admin.site.register(Story, StoryAdmin)

