from django.contrib import admin
from app.models import CustomUser, Tweet

class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ('admin_thumbnail','username','email','last_update','last_login',
        'activity_interval','publish_interval','mail_interval','half_dead', 'dead', 'admin_posts')
    search_fields = ('username', 'email')
    list_display_links = ('admin_thumbnail','username','email')

admin.site.register(CustomUser, CustomUserAdmin) 
    
class TweetAdmin(admin.ModelAdmin):
    list_display = ('text','pub_date','user')
    list_filter = ('user',)
    
admin.site.register(Tweet, TweetAdmin) 
